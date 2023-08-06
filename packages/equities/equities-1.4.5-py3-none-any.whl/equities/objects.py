import os 
import sys 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from equities.lib.access.DataAccessor import DataAccessor
from equities.scripts.orchestra.pull  import pull

from equities.scripts import test

decorator = ("="*50,"="*50)

class Universe(object):

    def __init__(self):
        try:
            self.da = None
            self.ciks = None
            self._initialize_da()
        except:
            pass
        
    def __getitem__(self,id):
        return Company(cik = str(id),da = self.da)

    def __len__(self):
        return len(self.ciks)

    def _initialize_da(self):
        self.da = DataAccessor()
        self.ciks = list(self.da.get(item = 'properties').T['cik'])
        print(" > 🌟 ( universe instantiated ) - local storage connected")

    def properties(self):
        ''' Gets properties df '''
        return self.da.get('properties')

    def manifest(self):
        ''' Gets manifest df '''
        return self.da.get('manifest')


    def download(self,quarters=[],ciks=[]):
        print(">>> BUILDING SEC UNIVERSE")
        puller = pull()
        puller.execute_pipeline(quarters = [q.lower() for q in quarters],
                                ciks = ciks)
        self._initialize_da()

    def purge(self):
        print(">>> PURGING SEC UNIVERSE")
        puller = pull()
        puller.purge_pipeline()
        print(">>> complete")


    def test(self):
        test.execute()

class Company(object):

    def __init__(self,cik,da,collapse=False):
        self.collapse = collapse
        self.cik      = cik
        self.da       = da
            
    def _header_series(self):
        ''' gets cik queried properties df'''
        return self.da.get(item = 'properties')[int(self.cik)]

    def _try_sheet(self,item):
        '''  Attempts to get a Sheet from 
        data accessor object. This object
        is super important, just know that
        it can be used to grab items from 
        'data/clean'. '''
        try:
            result = self.da.get(item = item,
                                 cik  = self.cik,
                                 collapse = self.collapse)
        except Exception as e:
            print(e)
            result = None
        return  result


    def name(self):
        ''' gets company name '''
        return self._header_series()['name']

    def sic(self):
        ''' gets sic number '''
        return int(self._header_series()['sic'])

    def division(self):
        ''' gets division name '''
        try: return self.da.resolver.resolve(\
                int(self.sic),'SIC','Division')
        except: return 'N/A';

    def industry(self):
        ''' gets industry name ''' 
        try:  return self.da.resolver.resolve(\
                int(self.sic),'SIC','Industry Group')
        except: return 'N/A';

    ''' Sec Data Sheets '''
    def income(self):
        # Gets income statement. 
        return self._try_sheet(item = 'income')

    def balance(self):
        # Gets balance sheet.
        return self._try_sheet(item = 'balance')

    def cash(self):
        # Gets cash flow statement.
        return self._try_sheet(item = 'cash')

    def equity(self):
        # Gets equity sheet.
        return self._try_sheet(item = 'equity')

    def undefined(self):
        # Gets undefined sheet. 
        return self._try_sheet(item = 'undefined')  
        