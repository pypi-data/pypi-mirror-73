import os
import sys
import shutil
import json
import pickle
import requests
import time
import zipfile
import difflib
from io import BytesIO
from datetime import datetime

import pandas as pd
import numpy as np

from tqdm import tqdm

import wikipedia

class waiter(object):
    '''
        Description: The waiter library is a small class that handles our data
        feeds. In particular the waiter class allows you to download all raw
        data to equities/data/... Currently libraries using the waiter:
        1) equities/lib/sec
        2) equities/lib/yahoo
    '''

    def __init__(self,data_config = {}):

        # Get data and library directories.
        try :    self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except : self.LIBDIR  = os.getcwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','wikipedia')

        self.search_terms = []

        # Sets dataconfig
        default_config = {'wikipedia':{
                                'company_names': [],
                                'sentence_count': 1
                             }
                         }
        self.data_config = data_config if data_config != {} else default_config

        # Generates initialization manifest from data config
        #self._generate_manifest()

        # Makes direcotires
        

    def _divide_chunks(self,array, n):
        '''
            Returns array of arrays of input with. sub arrays have length n. '''
        for i in range(0, len(array), n):
            yield array[i:i + n]


    def _mk_dirs(self,tickers):
        '''
            Makes necessary data directory structures for downloading
            data.  '''
    
        # Makes yahoo directory in equities/lib/data.
        if 'wikipedia' not in os.listdir(os.path.join(self.LIBDIR,'..','..','..','data')):
            os.mkdir(os.path.join(self.LIBDIR,'..','..','..','data','wikipedia'))

        # Makes clean and raw folders
        for directory in ['summary','links']:
            if directory not in os.listdir(os.path.join(self.DATADIR)):
                os.mkdir(os.path.join(self.DATADIR,directory))

    def download_data(self,
            company_names     = [],
            test              = False):

        company_name_array = company_names if company_names != [] else self.data_config['wikipedia']['company_names']

        self._mk_dirs(company_name_array)

        desc = '\t\t> Downloading Wikipedia Data... ';print(desc)

        # Master Download Bundles
        
        for cik,company_name in tqdm(company_name_array,desc = desc.ljust(40),ncols = 115):

            # Searches wikipedia
            search_arr    = wikipedia.search(company_name)
            
            case_mapping = dict(zip(search_arr,[x.lower() for x in search_arr]))
            #print(company_name)
            try: 
                # Computes closest match to company name
                search_result = case_mapping[difflib.get_close_matches(company_name.lower(),search_arr,1)[0]]
                # Gets wikipedia page summary. 
                company_summary = wikipedia.summary(search_result,self.data_config['wikipedia']['sentence_count'])
                time.sleep(0.2)
                # Gets wikipedia page links
                company_links = wikipedia.page(search_result).links            
            except:
                company_links  = None
                company_summary = None
            # Saves summary text 
            if company_summary != None:
                with open(os.path.join(self.DATADIR,'summary',str(cik) + '_summary.txt'),'w',encoding='utf-8') as tf:
                    tf.write(str(company_summary))
            
            if company_links != None:
                pd.Series(company_links).to_csv(os.path.join(self.DATADIR,'links',str(cik) + '_links.csv'),encoding='utf-8')
            time.sleep(0.1)
            
    def purge_data(self):
        '''
            Deletes all data downloaded using the self.download_database()
            method.

            args:
                1) quarter_array - array of quarters to purge. If this
                   variable defaults to [], all quarters avaliable are
                   deleted.
        '''
        # Computes quartes to purge.
        desc = '> Purging Wikipedia Data...'
        for dataitem in tqdm(os.listdir(os.path.join(self.DATADIR,'links','raw')),desc = desc.ljust(40),ncols=85):
            try: shutil.rmtree(os.path.join(self.DATADIR,'raw',dataitem))
            except: pass
        '''
        for purge_quarter in tqdm(purge_quarters,\
        desc='Purging data in' + str(os.path.join(self.DATADIR,'raw_txt'))):
            try: shutil.rmtree(os.path.join(self.DATADIR,'raw_txt',purge_quarter))
            except: pass'''

if __name__ == "__main__":

    w = waiter()
    company_names = [('1124212','Apple Inc'), ('1214241','Alphabet Inc')]
    w.data_config = {'wikipedia': {'company_names': company_names, 'sentence_count' : 10}}
    w.download_data(company_names = company_names)