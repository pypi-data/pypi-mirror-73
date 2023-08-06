import os
import sys
import shutil
import json
import pickle
import requests
import zipfile
from io import BytesIO
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

#from yahoofinancials import YahooFinancials

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
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','yahoo')

        self.ticker_array = []

        # Sets dataconfig
        default_config = {'yahoo':
                            {'stmts': ['income','balance','cash'],
                             'freqs': ['annual','quarterly'],
                             'ticks': self.ticker_array,
                             'min_date': '2000-01-01',
                             'max_date': datetime.today().strftime("%Y-%m-%d"),
                             'call_threshold':10,
                             'financial_statements':False,
                             'pit_price':False,
                             'ts_price':True,
                             'summary':False,
                             'statistics':False,
                             'eps':False,
                             'shares_outstanding':False,
                             'av_shares_outstanding':False
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
        ''
        # Makes yahoo directory in equities/lib/data.
        if 'yahoo' not in os.listdir(os.path.join(self.LIBDIR,'..','..','..','data')):
            os.mkdir(os.path.join(self.LIBDIR,'..','..','..','data','yahoo'))

        # Makes clean and raw folders
        for dir in ['raw','clean']:
            if dir not in os.listdir(os.path.join(self.DATADIR)):
                os.mkdir(os.path.join(self.DATADIR,dir))

        '''# Makes ticker and quarter/annual direcotories
        for ticker in tickers:
            if ticker not in os.listdir(os.path.join(self.DATADIR,'raw')):
                os.mkdir(os.path.join(self.DATADIR,'raw',str(ticker)))
            for dir in ['quarter','annual']:
                if dir not in os.listdir(os.path.join(self.DATADIR,'raw',str(ticker))):
                    os.mkdir(os.path.join(self.DATADIR,'raw',ticker,dir))'''



    def download_data(self,
            tickers     = [],
            bundle_size = 10,
            test        = False):

        ticker_array = tickers if tickers != [] else self.data_config['yahoo']['ticks']

        self._mk_dirs(ticker_array)

        desc = '\t\t> Downloading Yahoo Data... ';print(desc)

        # Master Download Bundles
        raw_pit_price         = {}
        raw_ts_price          = {}
        raw_summary           = {}
        raw_key_statisics     = {}
        raw_eps               = {}
        shares_outstanding    = {}
        av_shares_outstanding = {}

        # Bundle tickers into list of list of sizes bundle_size
        ticker_bundles = list(self._divide_chunks(tickers,bundle_size))
        #print(len(ticker_bundles))
        #print(len(ticker_bundles[0]))

        for ticker_bundle in tqdm(ticker_bundles,desc = desc.ljust(40),ncols=85):

            yf= YahooFinancials(ticker_bundle)

            '''try:
                if self.data_config['yahoo']['pit_price']:
                    raw_pit_price = {**raw_pit_price,**yf.get_stock_price_data()}
            except Exception as e:
                print(str(e))'''
            try:
                if self.data_config['yahoo']['ts_price']:
                    raw_ts_price = {**raw_ts_price,**yf.get_historical_price_data(
                                                   self.data_config['yahoo']['min_date'],
                                                   self.data_config['yahoo']['max_date'],
                                                   'daily')}
            except Exception as e:
                pass
                #print(str(e))
            '''try:
                if self.data_config['yahoo']['summary']:
                    raw_summary = {**raw_summary, **yf.get_summary_data()}
            except Exception as e:
                print(str(e))
            try:
                if self.data_config['yahoo']['statistics']:
                    raw_key_statisics = {**raw_key_statistics, **yf.get_key_statistics_data()}
            except Exception as e:
                print(str(e))
            try:
                if self.data_config['yahoo']['eps']:
                    raw_eps =  {**raw_eps,**yf.get_earnings_per_share()}
            except Exception as e:
                print(str(e))
            try:
                if self.data_config['yahoo']['shares_outstanding']:
                    shares_outstanding = {**shares_outstanding, **yf.get_num_shares_outstanding()}
            except Exception as e:
                print(str(e))
            try:
                if self.data_config['yahoo']['av_shares_outstanding']:
                    av_shares_outstanding = {**av_shares_outstanding,**yf.get_num_shares_outstanding(price_type = 'average')}
            except Exception as e:
                print(str(e))'''

        '''# Reads in data 
        with open(os.path.join(self.DATADIR,'raw','pit_price.pickle'), 'rb') as handle:
            pit_price_data = pickle.load(handle)

        with open(os.path.join(self.DATADIR,'raw','ts_price.pickle'), 'rb') as handle:
            ts_price_data = pickle.load(handle)

        with open(os.path.join(self.DATADIR,'raw','summary.pickle'), 'rb') as handle:
            summary_data = pickle.load(handle)

        with open(os.path.join(self.DATADIR,'raw','key_statistics.pickle'), 'rb') as handle:
            key_statistics_data = pickle.load(handle)

        with open(os.path.join(self.DATADIR,'raw','eps.pickle'), 'rb') as handle:
            eps_data = pickle.load(handle)'''

        # Saves Merged Bundle Data 


        with open(os.path.join(self.DATADIR,'raw','ts_price.pickle'), 'wb') as pf:
            if raw_ts_price != {}:
                pickle.dump(raw_ts_price, pf, protocol=pickle.HIGHEST_PROTOCOL)


        return raw_ts_price
            

        # Financial Statement
        #try:
        #    if self.data_config['yahoo']['financial_statements']:
        #        [stmts,freqs] = manifest_data # Unpacks manifest data for financial statements.
        #        raw_financial_statements = yahoo_company.get_financial_stmts(freqs,stmts)
        #        with open(os.path.join(self.DATADIR,'raw',tick,'financial_statements.pickle'), 'wb') as pf:
        #            pickle.dump(raw_financial_statements, pf, protocol=pickle.HIGHEST_PROTOCOL)
        #except Exception as e:
        #    print(str(e))

        # PIT Price Data
        '''
        try:
            if self.data_config['yahoo']['pit_price']:
                raw_pit_price = yahoo_company.get_stock_price_data()
                with open(os.path.join(self.DATADIR,'raw',tick,'pit_price.pickle'), 'wb') as pf:
                    pickle.dump(raw_pit_price, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # TS Pirce Data
        try:
            if self.data_config['yahoo']['ts_price']:
                raw_ts_price = yahoo_company.get_historical_price_data('2000-01-01','2020-01-01','daily')
                with open(os.path.join(self.DATADIR,'raw',tick,'ts_price.pickle'), 'wb') as pf:
                    pickle.dump(raw_ts_price, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # Summary information
        try:
            if self.data_config['yahoo']['summary']:
                raw_summary = yahoo_company.get_summary_data()
                with open(os.path.join(self.DATADIR,'raw',tick,'summary.pickle'), 'wb') as pf:
                    pickle.dump(raw_summary, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # Key statisics
        try:
            if self.data_config['yahoo']['statistics']:
                raw_key_statisics = yahoo_company.get_key_statistics_data()
                with open(os.path.join(self.DATADIR,'raw',tick,'key_statistics.pickle'), 'wb') as pf:
                    pickle.dump(raw_key_statisics, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # Earnings per share
        try:
            if self.data_config['yahoo']['eps']:
                raw_eps =  yahoo_company.get_earnings_per_share()
                with open(os.path.join(self.DATADIR,'raw',tick,'eps.pickle'), 'wb') as pf:
                    pickle.dump(raw_eps, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # Number of shares outstanding
        try:
            if self.data_config['yahoo']['shares_outstanding']:
                shares_outstanding = yahoo_company.get_num_shares_outstanding()
                with open(os.path.join(self.DATADIR,'raw',tick,'shares_outstanding.pickle'), 'wb') as pf:
                    pickle.dump(shares_outstanding, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

        # Average number of shares outstanding.
        try:
            if self.data_config['yahoo']['av_shares_outstanding']:
                av_shares_outstanding = yahoo_company.get_num_shares_outstanding(price_type = 'average')
                with open(os.path.join(self.DATADIR,'raw',tick,'average_shares_outstanding.pickle'), 'wb') as pf:
                    pickle.dump(av_shares_outstanding, pf, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))
        '''


    def update_data(self,data_item,bundle_size = 10):
        in_path = os.path.join(self.DATADIR,data_item+'.pickle')

        with open(in_path, 'rb') as handle:

            # Load Data Item
            data = pickle.load(handle)

            if data_item == 'ts_price':
                tickers = [ticker for ticker in data.keys()]
                self.download_data(tickers = tickers,
                                   bundle_size = bundle_size)

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
        desc = '> Purging Yahoo Data...'
        for dataitem in tqdm(os.listdir(os.path.join(self.DATADIR,'raw')),desc = desc.ljust(40),ncols=85):
            try: shutil.rmtree(os.path.join(self.DATADIR,'raw',dataitem))
            except: pass
        '''
        for purge_quarter in tqdm(purge_quarters,\
        desc='Purging data in' + str(os.path.join(self.DATADIR,'raw_txt'))):
            try: shutil.rmtree(os.path.join(self.DATADIR,'raw_txt',purge_quarter))
            except: pass'''
