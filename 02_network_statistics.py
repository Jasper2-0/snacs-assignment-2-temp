#!/usr/local/bin/python

import sys 
reload(sys) 
sys.setdefaultencoding("UTF-8")

import networkx as nx
import numpy as np
import cPickle as pickle

import csv

from graph_tool.all import *

# /data is assumed to hold the provided graphs.

tinyFn = "csv/twitter-el-tiny.csv" # tiny network, for learning / debugging purposes
smallFn = "csv/twitter-el-small.csv"
largeFn = "csv/twitter-el-large.csv"

elGTTinyFn = "csv/twitter-el-gt-tiny.csv"
elGTSmallFn = "csv/twitter-el-gt-small.csv"
elGTLargeFn = "csv/twitter-el-gt-large.csv"

def main():

    DGTiny = parseEdgeFileToDiGraph(tinyFn)
    DGSmall = parseEdgeFileToDiGraph(smallFn)
    DGLarge = parseEdgeFileToDiGraph(largeFn)
    
    #numberOfEdges(DGTiny,'Tiny Network')
    #numberOfEdges(DGSmall,'Small Network')
    numberOfEdges(DGLarge,'Large Network')
    #
    #numberOfNodes(DGTiny,'Tiny Network')
    #numberOfNodes(DGSmall,'Small Network')
    numberOfNodes(DGLarge,'Large Network')
    #
    #networkDensity(DGTiny, 'Tiny Network')
    #networkDensity(DGSmall,'Small Network')
    networkDensity(DGLarge,'Large Network')
    
    #InDegreeDistribution(DGTiny,'Tiny Network', 'pickles/Tiny_In_Degree_Distribution.pickle')
    #InDegreeDistribution(DGSmall,'Small Network', 'pickles/Small_In_Degree_Distribution.pickle')
    InDegreeDistribution(DGLarge,'Large Network', 'pickles/Large_In_Degree_Distribution.pickle')
    
    #OutDegreeDistribution(DGTiny,'Tiny Network', 'pickles/Tiny_Out_Degree_Distribution.pickle')
    #OutDegreeDistribution(DGSmall,'Small Network', 'pickles/Small_Out_Degree_Distribution.pickle')
    OutDegreeDistribution(DGLarge,'Large Network', 'pickles/Large_Out_Degree_Distribution.pickle')
    
    #numberOfWeaklyConnectedComponents(DGTiny,'Tiny Network');
    #numberOfWeaklyConnectedComponents(DGSmall,'Small Network');
    numberOfWeaklyConnectedComponents(DGLarge,'Large Network');
    
    #numberOfStronglyConnectedComponents(DGTiny,'Tiny Network');
    #numberOfStronglyConnectedComponents(DGSmall,'Small Network');
    numberOfStronglyConnectedComponents(DGLarge,'Large Network');
    
    #largestT = max(nx.strongly_connected_component_subgraphs(DGTiny), key=len)
    #largestS = max(nx.strongly_connected_component_subgraphs(DGSmall), key=len)
    largestL = max(nx.strongly_connected_component_subgraphs(DGLarge), key=len)
    
    #largestComponentStats(largestT,'Largest Component Tiny Network','pickles/Largest_Tiny_In_Degree_Distribution.pickle')
    #largestComponentStats(largestS,'Largest Component Small Network','pickles/Largest_Small_In_Degree_Distribution.pickle')
    largestComponentStats(largestL,'Largest Component Large Network','pickles/Largest_Large_In_Degree_Distribution.pickle')
    
    #saveLargestComponent(largestT,"csv/twitter-largest-tiny.csv")
    #saveLargestComponent(largestS,"csv/twitter-largest-small.csv")
    #saveLargestComponent(largestL,"csv/twitter-largest-large.csv")

    #DGTiny = parseEdgeFileToGTDiGraph(elGTTinyFn)
    #DGSmall = parseEdgeFileToGTDiGraph(elGTSmallFn)
    #DGLarge = parseEdgeFileToGTDiGraph(elGTLargeFn)
    
    #DistanceDistribution(DGTiny,'pickles/Tiny_Distance_Histogram.pickle')
    #DistanceDistribution(DGSmall,'pickles/Small_Distance_Histogram.pickle')
    #DistanceDistribution(DGLarge,'pickles/Large_Distance_Histogram.pickle')

def numberOfEdges( Graph, Title ):
    print "### Number of edges"
    print Title +': '+ str( nx.number_of_edges(Graph) )
    print "\n"
    
def numberOfNodes ( Graph, Title ):
    print "### Number of Nodes in the network"
    print Title + ": " + str( nx.number_of_nodes(Graph) )   
    print "\n"
    
def networkDensity ( Graph, Title ):
    print "### Network Density"
    print Title + ": " + str( nx.density(Graph))  
    print "\n"

def InDegreeDistribution ( DiGraph, Title, Filename ):
    inDegrees = DiGraph.in_degree().values()
        
    InBinCount =  np.bincount(np.array(inDegrees))

    dump (InBinCount,Filename);    
    print "In Degree Distribution "+Title+" \n"
    print InBinCount
    print "\n"
    

def OutDegreeDistribution ( DiGraph, Title, Filename ):
    outDegrees = DiGraph.out_degree().values()
    OutBinCount = np.bincount(np.array(outDegrees))
    
    dump (OutBinCount,Filename);    
    
    print "Out Degree Distribution "+Title+" \n"
    print OutBinCount
    print "\n"
    
def numberOfWeaklyConnectedComponents ( Graph, Title ):
    print "Number of weakly connected components " 
    print Title + ": "+ str ( nx.number_weakly_connected_components(Graph) )
    print "\n"


def numberOfStronglyConnectedComponents ( Graph, Title ):
    print "Number of strongly connected components " 
    print Title + ": "+ str ( nx.number_strongly_connected_components(Graph) )
    print "\n"


def largestComponentStats (Graph, Title, Filename):
    numberOfEdges(Graph,Title)
    numberOfNodes(Graph,Title)
    networkDensity(Graph,Title)
    InDegreeDistribution(Graph,Title, Filename)
    OutDegreeDistribution(Graph,Title, Filename)
    
def saveLargestComponent(Graph,Filename):
    nx.write_weighted_edgelist(Graph,Filename,delimiter=",")   


def DistanceDistribution(Graph, Filename):
    l = graph_tool.topology.label_largest_component(Graph)
    u = graph_tool.topology.GraphView(Graph,vfilt=l)
    
    dist = graph_tool.stats.distance_histogram(u);
    
    dump(dist[0],Filename);
    
    print "Distance Distribution:"
    print dist[0]
    print "\n"


def parseEdgeFileToDiGraph( filename ):

    DG = nx.DiGraph()

    with open(filename,'r') as edgeFile:
        for line in edgeFile:
            line = line.rstrip('\n')
            v = line.split(",")
            
            DG.add_edge(v[0],v[1],{'weight':v[2],'timestamp':v[3]});

    return DG

def parseEdgeFileToGTDiGraph( filename ):

    G = Graph()
    
    with open(filename,'r') as edgeFile:
        fileReader = csv.reader(edgeFile, delimiter=',', quotechar='|')
        
        fileReader.next() # skip header
        
        for c in fileReader:
            G.add_edge(c[0],c[1])

    return G


def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))

main()