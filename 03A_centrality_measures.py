#!/usr/local/bin/python

import sys 
reload(sys) 
sys.setdefaultencoding("UTF-8")

import networkx as nx
import numpy as np
import cPickle as pickle
import csv

from graph_tool.all import *

from operator import itemgetter

from collections import Counter

import math

# /data is assumed to hold the provided graphs.

tinyFn = "csv/twitter-el-gt-tiny.csv" # tiny network, for learning / debugging purposes
smallFn = "csv/twitter-el-small.csv"
#largeFn = "csv/twitter-el-larger-ce.csv"

#elGTTinyFn = "csv/twitter-el-gt-tiny.csv"
#elGTSmallFn = "csv/twitter-el-gt-small.csv"
elGTLargeFn = "csv/twitter-el-gt-large.csv"

def main():

    G = Graph()

    vp_source_username = G.new_vertex_property("string")
    vp_target_username = G.new_vertex_property("string")
    vp_weight = G.new_vertex_property("int")
    vp_timestamp = G.new_vertex_property("int")
    
    with open(elGTLargeFn,'r') as edgeFile:
        fileReader = csv.reader(edgeFile, delimiter=',', quotechar='|')
        
        fileReader.next() # skip header
        
        for c in fileReader:
            
            srcID = c[0];
            tgtID = c[1];
            srcName = c[2];
            tgtName = c[3];
            
            G.add_edge(srcID,tgtID)
            
            vp_source_username[G.vertex(srcID)] = srcName;
            vp_target_username[G.vertex(tgtID)] = tgtName;
  
    closeness = graph_tool.centrality.closeness(G)
    
    cList = []
    
    for user in G.vertices():
        if closeness[user] > 0:
            cList += [(vp_source_username[user],closeness[user])]
    
    cList = sorted(cList,key=itemgetter(1),reverse=True)[:20]
    
    print "Closeness"
    
    for i in range(len(cList)):
        print cList[i][0]
    #
    #betweenness = graph_tool.centrality.betweenness(G)
    #bList = []
    #
    #print "Betweenness"
    #
    #for user in G.vertices():
    #    if betweenness[0][user] > 0:
    #        bList += [(vp_source_username[user],betweenness[0][user])]
    #
    #bList = sorted(bList,key=itemgetter(1),reverse=True)[:20]
    #
    #for i in range(len(bList)):
    #    print bList[i][0]
    #
    #
    #DGSmall = parseEdgeFileToDiGraph(smallFn)
    #idg = nx.in_degree_centrality(DGSmall);
    #idList = []
    #
    #for user in idg:
    #    idList += [(user,idg[user])]
    #
    #print "In Degree Distribution"
    #idList = sorted(idList,key=itemgetter(1),reverse=True)[:20]
    #
    #for i in range(len(idList)):
    #    print idList[i][0]
    #
    #
    #odg = nx.out_degree_centrality(DGSmall);
    #
    #odList = []
    #
    #for user in odg:
    #    odList += [(user,odg[user])]
    #
    #print "Out Degree Distribution"
    #odList =  sorted(odList,key=itemgetter(1),reverse=True)[:20]
    #
    #for i in range(len(odList)):
    #    print odList[i][0]
    
    
def parseEdgeFileToDiGraph( filename ):

    DG = nx.DiGraph()

    with open(filename,'r') as edgeFile:
        for line in edgeFile:
            line = line.rstrip('\n')
            v = line.split(",")
            
            DG.add_edge(v[0],v[1],{'weight':v[2],'timestamp':v[3]});

    return DG    

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


def dump(pickleVar, filename ):
    pickle.dump( pickleVar , open(filename,'wb'))

main()