import sys
import os
import pickle 

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tqdm import tqdm

class Universe(object):


    def __init__(self,tickers = [],build = False):

        # Define internal raw data map
        self.map       = {}
        self.tickers    = tickers

        # Jupyter notebook patch
        try:    self.LIBDIR = os.path.dirname(os.path.real(__file__))
        except: self.LIBDIR = os.getcwd();pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','data','yahoo')

        # Indexable Files

        self.indexable_files = [
            'ts_price.pickle'
        ]
        
        '''self.indexable_files = [
            'financial_statements.pickle',
            'pit_price.pickle',
            'ts_price.pickle',
            'summary.pickle',
            'key_statistics.pickle',
            'eps.pickle',
            'shares_outstanding.pickle',
            'average_shares_outstanding.pickle'
            ]'''

        if build:
            self.build()

    def __getitem__(self,i):
        return self.map[i]

    def len(self):
        return len(self.map.keys())


    def _parse_dataitem(self,data_item):

        parse_output = {file:{} for file in self.indexable_files}
        file_path = os.path.join(self.DATADIR,'raw',data_item)
        data_tag = data_item.replace('.pickle','')

        if data_tag == 'ts_price':
            self.map['ts_price'] = self._parse_ts_price(data_tag)
        else:
            print('Critical Error, unrecognized Data Tag --- quitting')
            quit()

    def _parse_ts_price(self,data_tag):

        # Convert to pandas timestamp
        date_convert = lambda x : pd.Timestamp(year  = int(x.split('-')[0]),
                                               month = int(x.split('-')[1]),
                                               day   = int(x.split('-')[2]))
        # Open Price data

        desc = '\t - Parsing ts_price'

        ts_price = {}
        in_path = os.path.join(self.DATADIR,'raw',data_tag+'.pickle')

        with open(in_path, 'rb') as handle:
            
            # Load Raw TS price data 
            raw_ts_price = pickle.load(handle)

            for ticker,data in tqdm(raw_ts_price.items(),desc = desc.ljust(40),ncols=85):

                # Creates output_format
                ts_price[ticker] = {k:None for k in ['prices','dividends','splits']}

                # Extracts Price Data 
                try:
                    df = pd.DataFrame(raw_ts_price[ticker]['prices'])
                    df['formatted_date'] = df['formatted_date'].apply(date_convert)
                    df.set_index('formatted_date',inplace = True)
                    df.sort_index(axis = 1,inplace = True)
                    df.drop(['date','volume'],axis = 1,inplace = True) #
                    ts_price[ticker] = {'prices':df}
                except:
                    pass

                try:
                    # Extracts Dividend Data
                    df = pd.DataFrame(raw_ts_price[ticker]['eventsData']['dividends']).T
                    df['formatted_date'] = df['formatted_date'].apply(date_convert)
                    df.set_index('formatted_date',inplace = True)
                    df.sort_index(axis = 1,inplace = True)
                    df.drop(['date'],axis = 1,inplace = True) #
                    ts_price[ticker] = {**ts_price[ticker],**{'dividends':df}}
                except Exception as e:
                    #print(e)
                    pass

        return ts_price


    def build(self):
        # Builds Universe by parsing all indexable files
        for indexable_file in self.indexable_files:
            self._parse_dataitem(indexable_file)