import os
import sys

import pandas as pd 
import numpy as np 
class Company(object):
    '''
        Description: The waiter library is a small class that handles our data
        feeds. In particular the waiter class allows you to download all raw
        data to equities/data/... Currently libraries using the waiter:
        1) equities/lib/sec
        2) equities/lib/yahoo
    '''

    def __init__(self,cik):

        # Get data and library directories.
        try :    self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except : self.LIBDIR  = os.getcwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','wikipedia')
        self.cik = cik

        # Read Summary 
        with open(os.path.join(self.DATADIR,'summary',str(self.cik)+'_summary.txt'),'r') as f:
            self.summary = f.read()

        # Read Links 
        self.links = list(pd.read_csv(os.path.join(self.DATADIR,'links',str(self.cik)+'_links.csv'))['0'])
        

    def to_txt(self):
        with open(os.path.join(self.DATADIR,'..','clean',str(self.cik),'summary.txt'),'w+') as f:
            f.write(self.summary)

        #print(self.links)
        with open(os.path.join(self.DATADIR,'..','clean',str(self.cik),'links.txt'),'w+') as f:
            for elem in self.links:
                f.write(elem+'\n')
 


if __name__ == "__main__":

    c = Company(cik = '40987')
    c.to_txt()
    