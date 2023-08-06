import os 
import sys 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# Access objects
from equities.lib.access.DataAccessor import DataAccessor

# Scripts 
from equities.scripts.orchestra.pull  import pull
from equities.scripts import test

class Universe(object):
    '''
        A Universe should be thought of as a set of Companies.
        The universe object gives us the ability to download,
        access and purge our data. 
    '''

    def __init__(self):
        try:
            self.connect() # Connect to local storage.
            print(" > 🌟 ( universe instantiated ) - local storage connected")
        except:
            print(" > ⭐ ( universe instantiated ) - storage not connected or no data downloaded")
            pass
        
    def __getitem__(self,id):
        ''' 
            Universes are indexable by cik numbers,
            a company object is returned
        '''
        return Company(\
            cik = str(id),\
            da = self.da)

    def __len__(self):
        ''' 
            Returns number of companies 
            in local storage 
        '''
        if self.ciks == None: return 0
        else: return len(self.ciks)

    def connect(self):
        '''
            Connect to local storage by instantiating a data access
            object. recompute internal ciks arr.
        '''
        self.da = DataAccessor() # Data access object
        self.ciks = list(self.da.get(item = 'properties').T['cik'])
        

    def properties(self):
        ''' 
            Gets properties.json df     
        '''
        return self.da.get('properties')

    def manifest(self):
        ''' 
            Gets manifest.json df
        '''
        return self.da.get('manifest')

    def download(self,quarters=[],ciks=[]):
        '''
            Download sec data to local storage
        '''
        print(">>> BUILDING SEC UNIVERSE")
        pull().execute_pipeline(quarters = [q.lower() for q in quarters],
                                ciks = ciks)
        self.connect() # reconnects to update data

    def purge(self):
        '''
            Delete sec data from local storage
        '''
        print(">>> PURGING SEC UNIVERSE")
        pull().purge_pipeline()
        print(">>> complete")


    def test(self):
        '''
            Test function. See pypi documentation. 
        '''
        test.execute()


    def serialize(self):
        print(">>> SERIALIZING SEC UNIVERSE")
        print(" > 📦 ( packaging your universe )")
        uni = {}
        for cik in self.ciks:
            stmt = {}
            try: stmt['income']=self.__getitem__(cik).income()
            except: stmt['income']=None; pass
            try: stmt['balance']=self.__getitem__(cik).income()
            except: stmt['balance']=None; pass
            try: stmt['cash']=self.__getitem__(cik).cash()
            except: stmt['cash']=None; pass
            uni[cik]=stmt
        print(">>> complete")
        return uni
        




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

    ''' 
        Sec Data Sheets 
    '''

    def income(self):
        # Gets income statement. 
        return self._try_sheet(\
            item = 'income')

    def balance(self):
        # Gets balance sheet.
        return self._try_sheet(\
            item = 'balance')

    def cash(self):
        # Gets cash flow statement.
        return self._try_sheet(\
            item = 'cash')

    def equity(self):
        # Gets equity sheet.
        return self._try_sheet(\
            item = 'equity')

    def undefined(self):
        # Gets undefined sheet. 
        return self._try_sheet(\
            item = 'undefined')  
        