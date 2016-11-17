#!/usr/local/bin/python
import sys 
reload(sys) 
sys.setdefaultencoding("UTF-8")

from datetime import datetime, time
import csv

# ttp / twitter-text-python is a python library for parsing tweets
# https://github.com/edburnett/twitter-text-python
#
# it's based on twitter's standardized tweet parsing library.
# https://github.com/twitter/twitter-text

from ttp import ttp

tinyFn = "data/twitter-tiny.in" # tiny set, for learning / debugging purposes
smallFn = "data/twitter-small.in" # small set
largeFn = "data/twitter-larger.in" # larger set

elTinyFn = "csv/twitter-el-tiny.csv"
elSmallFn = "csv/twitter-el-small.csv"
elLargeFn = "csv/twitter-el-large.csv"

elGTTinyFn = "csv/twitter-el-gt-tiny.csv"
elGTSmallFn = "csv/twitter-el-gt-small.csv"
elGTLargeFn = "csv/twitter-el-gt-large.csv"

elFiltTinyFn = 'csv/twitter-el-filtered-tiny.csv'
elFiltSmallFn = 'csv/twitter-el-filtered-small.csv'
elFiltLargeFn = 'csv/twitter-el-filtered-large.csv'

elFiltGTTinyFn = 'csv/twitter-el-filtered-gt-tiny.csv'
elFiltGTSmallFn = 'csv/twitter-el-filtered-gt-small.csv'
elFiltGTLargeFn = 'csv/twitter-el-filtered-gt-large.csv'

def main():

    adjTiny = createAdjacencyList(tinyFn)
    #adjSmall = createAdjacencyList(smallFn)
    #adjLarge = createAdjacencyList(largeFn)
    
    createEdgeList(adjTiny,elTinyFn);
    #createEdgeList(adjSmall,elSmallFn);
    #createEdgeList(adjLarge,elLargeFn);
    
    createGTEdgeList(adjTiny,elGTTinyFn);
    #createGTEdgeList(adjSmall,elGTSmallFn);
    #createGTEdgeList(adjLarge,elGTLargeFn);



def createAdjacencyList(inputFile):
    p = ttp.Parser()
    
    # create an adjacency list
    
    adjacencyList = {}
        
    with open(inputFile,'r') as twitterFile:
        for line in twitterFile:

            line = line.rstrip('\n')
            t = line.split("\t")

            timestamp = int(datetime.strptime(t[0],"%Y-%m-%d %H:%M:%S").strftime("%s"))
            username = t[1]
            mentionedUsers = p.parse(t[2],html=False).users
            
            if len(mentionedUsers) > 0:

                if username not in adjacencyList:
                    adjacencyList[username] = {}

                for m in mentionedUsers:
                    if m not in adjacencyList[username]:
                        adjacencyList[username][m] = {}
                        adjacencyList[username][m]['timestamps'] = [timestamp]
                    else:
                        adjacencyList[username][m]['timestamps'] += [timestamp]

                    adjacencyList[username][m]['timestamps'].sort()
                    adjacencyList[username][m]['firstMention'] = adjacencyList[username][m]['timestamps'][0]
                    adjacencyList[username][m]['numberOfMentions'] = len(adjacencyList[username][m]['timestamps'])
    
    return adjacencyList

def createEdgeList(adjacencyList,filename):
    # create and edge list for gephi
                    
    edgeList = []

    for user in adjacencyList:
        for mentionedUser in adjacencyList[user]:
            weight = adjacencyList[user][mentionedUser]['numberOfMentions']
            timestamp = adjacencyList[user][mentionedUser]['firstMention']
            edgeList += [(user,mentionedUser,weight,timestamp)]

    with open(filename,'wb') as edgelist_file:
        csvOut = csv.writer(edgelist_file)
        csvOut.writerow(['Source','Target','Weight','Timestamp']);
        for row in edgeList:
            csvOut.writerow(row)

def createGTEdgeList(adjacencyList,filename):
    # create and edgelist for graph-tool (graph-tool wants integers for IDs)

    users = []

    for user in adjacencyList:
        users += [user];
        for mentionedUser in adjacencyList[user]:
            users += [mentionedUser]
        
    users = list(set(users))
    uTuple = []

    for i in range(len(users)):
        uTuple+= [(users[i],i)]

    uDict = {}

    for u in uTuple:
        uDict[u[0]] = u[1]

    edgeList = []

    for user in adjacencyList:
        for mentionedUser in adjacencyList[user]:
            weight = adjacencyList[user][mentionedUser]['numberOfMentions']
            timestamp = adjacencyList[user][mentionedUser]['firstMention']
            edgeList += [(uDict[user],uDict[mentionedUser],user,mentionedUser,weight,timestamp)]
    
    with open(filename, 'wb') as edgelist_gt_file:
        csvOut = csv.writer(edgelist_gt_file)
        csvOut.writerow(['Source','Target','Source-Username','Target-Username','Weight','Timestamp']);
        for row in edgeList:
            csvOut.writerow(row)

main()