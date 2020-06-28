#!python 3 
#Utilises PRAW v7.0 to analyse the top posts of AmItheAsshole subreddit

import os
import praw
import logging
import sys, re
import pandas as pd
import datetime
import numpy as np
from matplotlib import pyplot as plt
from RequestParameters import RequestParameters
from SubDataController import SubDataController
from AnalysisHelper import AnalysisHelper

def main():
    
    #input parameters
    agent = "Subreddit Metrics Gathering"
    requestParam = RequestParameters("amitheasshole",100,'top')
    
    subData = SubDataController(agent,requestParam,True)
    #subData.getSubmissions()
    
    #regex to remove META and Update posts    
    #flairRegex = re.compile(
    r'''
    #Asshole
    (asshole)| 
    
    #Everyone Sucks
    (everyone\ sucks)|
    
    #not the a-hole
    (not\ the\ a-hole)|
    
    #no ahole 
    (no\ a-holes\ here)
    
    '''
    #,re.X | re.I )
    
    #subData.filterPostsFlair(flairRegex)
    
    
    #Save the required info to a file
    fileName = subData.generateFileName(requestParam)

    folderName = "SubredditData"
    
    #subData.saveToFile(fileName, folderName)
    subData.loadLocalData(fileName, folderName)

    df = subData.getDataFrame()
    analyser = AnalysisHelper()
    
    topWords = analyser.getTopWords(df)
    topWords = topWords.sort_values(by='count', ascending = False)
    # Make some nice summary graphs!
    fileName = "TopWords-amitheasshole-1000.csv"

    dfShort = topWords.iloc[1:25,:]
    
    dfShort.plot(x='word',y='count', kind = 'bar')
    plt.show()

    #TODO: unit testing of generic scripts
    
    
    
    #TODO: GUI!

if __name__ == '__main__':
    main()