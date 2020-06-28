#!python 3 
#Helper class to run functions that analyse reddit data in data frame form


import os
import praw
import logging
import sys, re
import pandas as pd
import datetime
import numpy as np



class AnalysisHelper:


    @staticmethod
    def getTopWords(df):
         
        counter = 0
        
        topWords = dict()
        
        firstWord = True
        
        for index, rowData in df.iterrows():
            #logging.info(counter)
            
            titleString = rowData.get("Title")
    
            
            for word in titleString.split():
                
                #TODO: MAke a regex for a word
                wordRegex = re.compile(
                    '''
                    
                    #remove symbols
                    (\w*)
                    
                    '''
                    ,re.RegexFlag.X | re.RegexFlag.I)
                
                wordMatch = re.search(wordRegex,word)
                
                word = wordMatch.group(1)
                
                
                
                if firstWord:
                    topWords[word] = 1
                    firstWord = False
                else:
                    if word in topWords: 
                    # Increment count of word by 1 
                        topWords[word] = topWords[word] + 1
                    else: 
                    # Add the word to dictionary with count 1 
                        topWords[word] = 1
                        
                            
            counter = counter + 1    
        return pd.DataFrame(topWords.items(), columns = ['word','count'])      
