import sys
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm

class Company(object):
    '''
    Description: Company objects are programatic representations of real
    life companies.

    The tickers assigns unique 'ticker' number to every
    public company in America. Concequently a company must take upon
    instatitiation a cik number.

    If a universe object is passed in and headers is set to True, some
    meta data from the universe about the company is computed and
    store internally in Company.header_df.

    Methods on the company objects always take in a universe as a final
    argument. This is because Company methods use the passed in universe
    to query certain dataframes within Universe.map. These methods then
    return formatted dataframes of the financial statements (Time Series
    and Point in time)

    Lastly, this class contains a method which allows the user to plot the
    company's financial statements over time.'''


    def __init__(self,  cik,
                 u      = None,
                 header = True):

        # Stores cik internally
        self.cik = cik

        # Get data and library directories.
        self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','sec')

        # Get's Company Header data from sub.dataframes
        if header and u != None: self.header_df = self.get_header_df(u)

    def _get_adsh(fik,yr):
        '''
            Returns ADSHs for company, these represent unique filings

            args:
                1) fik - filing identification key.
                2) yr  - year

            '''
        return '%s-%s-%s'%str(self.cik).zfill(10),\
            str(yr).zfill(2),str(fik).zfill(6)

    def get_header_df(self,u):
        '''
            Gets time series indexed meta data for company

            args:
                1) u - Universe object in which to make queries to.'''
        subdf_array = []
        for quarter,df in u.map.items():
            if 'sub' in quarter:
                subdf_array.append(df[df.cik == self.cik])
        return pd.concat(subdf_array,axis=0).sort_values('filed').set_index('filed')


    def get_pit_stmt_df(self,stmt,quarter,u):
        '''
            Makes point in time query to passed in universe,'u'. Returns dataframe
            of financial statement 'stmt' during quarter, 'quarter'

            args:
                1) stmt    - financial statement code
                2) quarter - str of quarter
                3) u       - Universe object in quick to make queries to.

            '''

        # Gets tag df
        tag_df = u.map[quarter+'_tag']

        # Selects company using cik number.
        sub_df = u.map[quarter+'_sub'][u.map[quarter+'_sub']['cik'] == self.cik]
        pre_df = u.map[quarter+'_pre'][u.map[quarter+'_pre']['cik'] == self.cik]
        num_df = u.map[quarter+'_num'][u.map[quarter+'_num']['cik'] == self.cik]

        # Query pre df from stmt tags
        if stmt != '*':
            pre_df = pre_df[pre_df['stmt'] == stmt]
            pre_df.sort_values('line',inplace = True)

        # Selects quarter
        sub_df = sub_df[sub_df['quarter'] == quarter]
        pre_df = pre_df[pre_df['quarter'] == quarter]
        num_df = num_df[num_df['quarter'] == quarter]

        # Get statment data
        num_df = num_df[num_df['tag'].isin(list(pre_df['tag']))]

        # Sets indicies to tag
        num_df = num_df.set_index('tag')
        pre_df = pre_df.set_index('tag')
        tag_df = tag_df.set_index('tag')

        # Adds in data from pre_df to num_df
        for column in ['stmt','line','report','plabel','negating']:
            tag_column_map  = dict(zip(pre_df.index,pre_df[column]))
            series_array    = list([tag_column_map[tag] for tag in num_df.index])
            num_df[column]  = pd.Series(series_array,index = num_df.index)

        # Adds in data from tag_df to num_df
        for column in ['tlabel','doc','crdr']:
            tag_column_map  = dict(zip(tag_df.index,tag_df[column]))
            series_array    = list([tag_column_map[tag] for tag in num_df.index])
            num_df[column]  = pd.Series(series_array,index = num_df.index)

        # Sorts num_df by line number
        num_df.sort_values('line',inplace = True)

        return num_df

    def get_ts_stmt_df(self,stmt,quarters,u,mute = False):
        '''
            Makes point in time query to passed in universe,'u'. Returns dataframe
            of a given financial statement 'stmt' for entire history of universe.

            args:
                1) stmt    - financial statement code.
                2) u       - Universe object in quick to make queries to.
            '''

        # Gets quarters in universe.
        desc = 'Generating statement df for (cik: %s,stmt: %s,quarters: %s,u.name: %s'\
        %(str(self.cik),stmt,str(quarters),str(u.name))
        quarter_array = quarters if quarters != [] \
        else list(set([elem.split('_')[0] for elem in u.map.keys()]))

        # Returns dataframe value map.
        quarter_series_map = {}

        # Iterates through quarters.
        for quarter in tqdm(quarter_array,desc = desc,disable = mute):

            # Gets PIT Statment dataframe.
            try:
                stmt_series = self.get_pit_stmt_df(stmt,quarter,u)['value']

                # Constructs value map.
                quarter_series_map[quarter] = dict(zip(stmt_series.index,list(stmt_series)))

            except:
                #print('Could not get ts data for quarter: %s'%(quarter))
                pass

        return pd.DataFrame(quarter_series_map)

    def to_csv(self,u):
        
        # Out directory
        out_path = os.path.join(self.DATADIR,'..','clean',str(self.cik))

        # Save stmts to csv
        stmt_array = u.stmt_array
        for stmt in stmt_array:
            ts_df = self.get_ts_stmt_df(stmt,[],u,mute = True)
            ts_df.to_csv(os.path.join(out_path,stmt+'.csv'))

        # Save header df 
        try:
            self.get_header_df(u).to_csv(os.path.join(out_path,'header.csv'))
        except Exception as e:
            print(e)
            pass

    def plot(self,u,show=False):
        '''
            Plots all company financial statements in time series view.

            args:
                1) show    - boolean. True => plt.show() will be called at the end
                                              of plotting.
                2) u       - Universe object in quick to make queries to.
            '''
        ax_map = {}

        # Iterates through possible financial statement codes.
        for stmt in u.stmt_array:
            try:
                # Gets time series dataframe and plot.
                title = str(self.cik)+'_'+stmt
                ts_df = self.get_ts_stmt_df(stmt=stmt,quarters=[],u=u).T
                ax = ts_df.plot(kind    = 'bar',
                                stacked = True,
                                figsize = (10,5),
                                title   = title,
                                legend  = False)
                                            
                # Stores matplotlib ax object in return map.
                ax_map[stmt] = ax
            except Exception as e:
                print(e)
                pass

        # Shows figures if specified.s
        if show: plt.show()

        return ax_map

    def financial_statement(self,stmt,quarters,u):
        '''
        Wrapper function for above methods Human Readable function with
        control flow to link point in timet/time series with quarter inputs.
        It takes in an array of quarter labels. If you pass in an array
        containing a single str quarter, you get the point in time result.
        Many quarters will give you the time series result.
        '''
        if quarters == []:
            quarter_array = list(set([elem.split('_')[0] for elem in u.map.keys()]))
        else:
            quarter_array = quarters
            

        if len(quarter_array) == 1:
            return self.get_pit_stmt_df(stmt,quarter_array[0],u)
        else:
            return self.get_ts_stmt_df(stmt,quarter_array,u)
