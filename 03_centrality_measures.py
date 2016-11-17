#!/usr/local/bin/python

import sys 
reload(sys) 
sys.setdefaultencoding("UTF-8")

import networkx as nx
import numpy as np
import cPickle as pickle




# /data is assumed to hold the provided graphs.

tinyFn = "csv/twitter-el-tiny-ce.csv" # tiny network, for learning / debugging purposes
smallFn = "csv/twitter-el-small-ce.csv"
largeFn = "csv/twitter-el-larger-ce .csv"

elGTTinyFn = "csv/twitter-el-gt-tiny.csv"
elGTSmallFn = "csv/twitter-el-gt-small.csv"
elGTLargeFn = "csv/twitter-el-gt-large.csv"

def main():

    DGTiny = parseEdgeFileToDiGraph(tinyFn)
    DGSmall = parseEdgeFileToDiGraph(smallFn)
#    DGLarge = parseEdgeFileToDiGraph(largeFn)

    print nx.in_degree_centrality(DGTiny)
    print nx.out_degree_centrality(DGTiny)
    
    
    print "\n"
    
    print nx.closeness_centrality(DGTiny)
    
#    print nx.betweenness_centrality(DGTiny,normalized=True,weight=None)
#    print nx.betweenness_centrality(DGSmall,normalized=True,weight=None)
    
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
        for line in edgeFile:
            line = line.rstrip('\n')
            v = line.split(",")
            
            G.add_edge(v[0],v[1])

    return G

def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))


main()