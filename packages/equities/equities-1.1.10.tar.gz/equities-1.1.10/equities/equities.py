import os 
import sys 

import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

from lib.access.DataAccessor import DataAccessor
from scripts.orchestra.pull  import pull


decorator = ("="*50,"="*50)

class Universe(object):

    def __init__(self):
        try:
            self.da = DataAccessor()

            self.ciks = list(\
            self.da.get(\
                item = 'properties').T['cik'])
        except:
            print("> Looks like you have no data yet. (Instantiate a universe and call download) or (run the build.sh script) to get data.")
            pass
        print("* equities universe instantiated.")
        
    def __getitem__(self,id):
        return Company(cik = str(id),da = self.da)

    def __len__(self):
        return len(self.ciks)

    def properties(self):
        ''' Gets properties df '''
        return self.da.get('properties')

    def manifest(self):
        ''' Gets manifest df '''
        return self.da.get('manifest')


    def download(self,quarters=[],num_companies=None):
        print("%s UNIVERSE DOWNLOADER SUMMONED %s"%(decorator))
        puller = pull()
        puller.execute_pipeline(quarters = [q.lower() for q in quarters],
                                num_companies = 50)
        print("%s UNIVERSE DOWNLOADER BANISHED %s"%(decorator))

    def purge(self):
        print("%s UNIVERSE PURGER SUMMONED %s"%(decorator))
        puller = pull()
        puller.purge_pipeline()
        print("%s UNIVERSE PURGER BANISHED %s"%(decorator))


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

    ''' Yahoo Data Sheets'''
    def prices(self):
        # Gets stock prices. 
        return self._try_sheet(item = 'prices')

    def dividends(self):
        # Gets dividends.
        return self._try_sheet(item = 'dividends')  

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

    ''' Wikipedia Data Sheets '''
    def summary(self):
        # Gets wikipedia summary.
        return self._try_sheet(item='summary')

    def links(self):
        # Gets wikipedia links
        return self._try_sheet(item='links')


    '''TODO: def _try_metric(self,funct,df):
    if type(df) != list:
        try: result = funct(df)
        except Exception as e: print(e); result = None
    else:
        try: result = funct(df[0],df[1])
        except Exception as e: print(e); result = None
    return result'''

    # TODO: Get Statistics
    '''def debt_to_equity(self):
    return self._try_metric(Metric.debt_to_equity,self.balance())
    def gross_profit_margin(self):
        return self._try_metric(Metric.gross_profit_margin,self.income())
    def return_on_equity(self):
        return self._try_metric(
            Metric.return_on_equity,[self.income(),self.balance()])'''


        
if __name__ == '__main__':

    c = Company(cik = '24741')
    print(c.income().columns)
    c.return_on_equity().plot(kind = 'bar',title = 'dte'); plt.show()