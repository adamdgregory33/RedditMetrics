#SubDataController - handles the saving, and compiling of data from subreddits
#contains non-subreddit specific access functions
#used for data extraction only

#Using PRAW v 7.0

import os
import praw
import logging
import sys, re
import pandas as pd
import datetime
import numpy as np
from matplotlib import pyplot as plt
from RequestParameters import RequestParameters




class SubDataController:
        
    #logLevel = logging.DEBUG
    logLevel = logging.INFO
    #logLevel = logging.CRITICAL
    logging.basicConfig(level = logLevel)
    
    
    reddit = None
    submissions = None
    readOnly = True
    requestParam = None
    processed = False
    
    #id, subreddit.id, title, score, upvote_ratio, num_comments,created_utc
    headers =["Post ID","Subreddit","Title","Score","Upvote Ratio", "Number of Comments","Time Created"]
    #set up data frame to store data
    df = pd.DataFrame(columns = headers)

    def __init__(self, agent, requestParam,readOnly = True):
        
        self.requestParam = requestParam
        self.agent = agent
        #"Subreddit Metrics Gathering"
        
        self.reddit = praw.Reddit(user_agent =agent)
        
        self.readOnly = readOnly
        self.reddit.read_only = self.readOnly
   

    def getDataFrame(self):
        return self.df
    
    def loadLocalData(self,fileName,folderName):
    
        #Open file
    
        self.df = pd.read_csv(folderName+'\\'+fileName, skipinitialspace = True)
    
   
    
    def getSubmissions(self):
        sub = self.requestParam.subName
        limit = self.requestParam.limit
        sortBy = self.requestParam.sortBy
        queryString = self.requestParam.queryString
        timeString = self.requestParam.timeString
        
        if queryString is '' and timeString is '':
            if sortBy is 'top':
                self.submissions = self.reddit.subreddit(sub).top(limit =limit)
            if sortBy is 'hot':
                self.submissions = self.reddit.subreddit(sub).hot(limit =limit)
        elif queryString is '' and timeString is not '':
            self.submissions=self.reddit.subreddit(sub).search(query ='',sort = sortBy,time_filter = timeString,limit = limit )
        elif queryString is not '' and timeString is '' :
            self.submissions = self.reddit.subreddit(sub).search(query =queryString,sort = sortBy,limit = limit )
        else:
            self.submissions = self.reddit.subreddit(sub).search(query =queryString,sort = sortBy,limit = limit , time_filter = timeString)

    #Filters posts by flair, adding data to the dataframe
    def filterPostsFlair(self,flairRegex = None):
        
        tempDf = pd.DataFrame(columns=  headers)
        
        for post in self.submissions:
        
            flairString = post.link_flair_text
            if flairString:
            
                #Remove META and update posts
                if not flairRegex in None and re.search(flairRegex,flairString):
                    
                    newline = (post.id, post.subreddit.name,post.title,post.score, post.upvote_ratio,post.num_comments, post.created_utc)
                    tepDf = tempDf.append(pd.Series(newline,index = tempDf.columns),ignore_index = True)
                    
                    logging.info(newline)
                elif flairRegex in None:
                    
                    newline = (post.id, post.subreddit.name,post.title,post.score, post.upvote_ratio,post.num_comments, post.created_utc)
                    tepDf = tempDf.append(pd.Series(newline,index = tempDf.columns),ignore_index = True)
                    
                    logging.info(newline)
                    
        
        self.df = tempDf
        addProcessedColumns()
        
    #add length of title column to data frame
    def addProcessedColumns(self):
        
        titleLengths = []
        for item in self.df.get(headers[headers.index("Title")]):
                titleLengths.append(len(item))
        
        self.headers.append('Title Length')
        
        self.df['Title Length'] = titleLengths
           
    #Saves subreddit data to a new local folder name of the user's choosing
    def saveToFile(self,fileName, folderName):
        
        #today = datetime.date.today().__str__()
        
        if not os.path.exists(folderName):
            
            os.makedirs(folderName)
            
        
        self.df.to_csv(folderName+'\\'+fileName,sep = ',',index = False)
        
        
        
    @staticmethod    
    def generateFileName(requestParam):
        separator = '-'
        filename = ''
        fileName = requestParam.subName+separator+requestParam.sortBy+separator+str(requestParam.limit)+'.csv'

        return fileName
    
    

        
     
   