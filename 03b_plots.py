import cPickle as pickle

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

SmallFn = "pickles/Small_Distance_Histogram.pickle"
LargeFn = 'pickles/Large_Distance_Histogram.pickle'


SmallBetweennessFn = "pickles/betweenness_centrality-small.pickle"

def main():
    
    
    SmallHistogram= pickle.load(open(SmallFn,'rb'))
    LargeHistogram = pickle.load(open(LargeFn,'rb'))
    
    SmallBetweenness = pickle.load(open(SmallBetweennessFn,'rb'))
    
    
    print SmallHistogram
    print LargeHistogram
    
    print len(SmallBetweenness)
    
main()