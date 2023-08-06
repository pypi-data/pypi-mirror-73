from io import BytesIO, StringIO
import multiprocessing
import threading
import sys
import os
import codecs
import time

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#from Company import Company
import emoji as emo
from tqdm import tqdm

class Universe(object):

    '''
    Description: The Universe object serves as a raw data bank for use
    by Company object methods. Upon initialization Universe searches:
    equities/data/sec/raw_txt for data downloaded by waiter.py.
    The universe object will then store all of this data in a map. '''


    def __init__(self,
                 quarters        = [],
                 multi_thread    = False,
                 build           = False,
                 cpu_load_factor = 20,
                 name            = None):
        '''
            Generate Internal map from raw txt data '''

        # Define internal map
        self.map             = {} # Universe objects are indexable by this map.
        self.multi_thread    = multi_thread
        self.cpu_load_factor = cpu_load_factor
        self.name            = name

        # Get data and library directories.
        try: self.LIBDIR = os.path.dirname(os.path.realpath(__file__))
        except Exception as e: self.LIBDIR = os.getcwd();pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','sec')

        # Generates list of in DATADIR.
        RAWDIR = os.path.join(self.DATADIR,'raw')
        dir_quarter_array = [elem for elem in os.listdir(RAWDIR) if elem != '.DS_Store']
        self.quarter_array = dir_quarter_array if quarters == [] else quarters

        # Hard coded list of possible statements.
        self.stmt_array    = ['IS','BS','CF','EQ']

        # Shrinkage 
        self.initial_size = self.size()

        # For some additional color / context:
        # 1) 'IS' - income statement
        # 2) 'BS' - balance sheet
        # 3) 'CF' - cashflow statement
        # 4) 'EQ' - comprehensive equity statement
        # 5) 'UN' - undefined

        # Builds on init if specified.
        if build:
            try:
                self.build(multi_thread = multi_thread)
            except:
                print('Multi-Threading Failed, attempting to self.build() on one thread..')
                self.build(multi_thread = False)
                pass

    def __getitem__(self, i):
        '''
            Access internal map '''
        return self.map[i]

    def __len__(self):
        '''
            Gets length of internal map '''
        return len(self.map.keys())

    def _get_threads(self):
        return int(multiprocessing.cpu_count())

    def _divide_chunks(self,array, n):
        '''
            Returns array of arrays of input with. sub arrays have length n. '''
        for i in range(0, len(array), n):
            yield array[i:i + n]

    def _parse_dataitem(self,quarter,data_item):
        '''
            Helper Method for parsing individual files. This
            function is multi_threaded in specified in the
            Universe constructor. '''

        # Constructs map label.
        label = '%s_%s'%(quarter,data_item.replace('.txt',''))

        # Reads in raw data dataframe.
        file_path = os.path.join(self.DATADIR,'raw',quarter,data_item)
        with codecs.open(file_path,'r',encoding='utf-8',errors='ignore') as f:
            # Reads in Table, focus on speed and, don't care too much about memory.
            self.map[label] = pd.read_table(f,
                                    sep             = '\t',
                                    lineterminator  = '\n',
                                    engine          = 'c',
                                    error_bad_lines = True,
                                    warn_bad_lines  = True,
                                    low_memory      = False,
                                    memory_map      = True)

        # Seperates out adsh into cik,yr, and fik columns.
        try: self.map[label][['cik','yr','fik']] \
             = self.map[label].adsh.str.split("-",expand=True)
        except Exception as e: pass

        # Applys integer cast to seperated adsh columns.
        try:
            for elem in ['cik','yr','fik']:
                self.map[label][elem]= self.map[label][elem].apply(\
                                                lambda x : int(x))
        except Exception as e: pass

        # Adds quarter label to data.
        self.map[label]['quarter'] = quarter

    def build(self):
        '''
            Parses raw data, structures it and cleans it. Alters internal,
            map self.map. '''

        pipeline_str = lambda emoji,x,total : ' > %s  ( '\
        %(str(emo.emojize(emoji,use_aliases=True)))+str(x)+' )'
        desc = pipeline_str(':boom:','expanding universe',0)
        success_count,total_count = 0,0

        dataitem_array  = ['num.txt','sub.txt','pre.txt','tag.txt']
        parse_arguments = [ (quarter,data_item) for quarter in self.quarter_array\
                                                for data_item in dataitem_array]
        # Multi_thread
        if self.multi_thread:

            # Instantiate thread_map
            thread_count = int(self.cpu_load_factor)
            thread_map   = {'thread_%s'%(str(ind)):None for ind in range(thread_count)}

            # Transform arguments by thread count.
            parse_bundle = self._divide_chunks(parse_arguments,thread_count)

            # Iterates through parsebundle and starts threads.
            for parse_arguments in parse_bundle:
                for ind,parse_argument in enumerate(parse_arguments):
                    quarter,data_item = parse_argument
                    if quarter != '.DS_Store':
                        try:
                            # Calls parse_dataitem placed on unpackaged parse args.
                            thread_map['thread_%s'%(str(ind))] = \
                            threading.Thread(target = self._parse_dataitem,
                                             args   = (quarter,data_item,))
                            success_count += 1
                        except Exception as e:
                            print('-- Error Could not parse Bundle element: %s'%(str(e)))
                            pass
                    total_count += 1
                # Start threads
                for ind,parse_argument in tqdm(enumerate(parse_arguments),desc = desc.ljust(40),ncols=85):
                    thread_map['thread_%s'%(str(ind))].start()

                # Wait for threads to join
                for ind,parse_argument in enumerate(parse_arguments):
                    thread_map['thread_%s'%(str(ind))].join()
        # Single Thread
        else:
            for quarter,data_item in tqdm(parse_arguments,desc = desc,ncols=85):
                if quarter != '.DS_Store':
                    try:
                        self._parse_dataitem(quarter,data_item)
                        success_count +=1
                    except Exception as e:
                        pass
                    total_count += 1

        #print('\t\t> Parsing and cleaning complete. elements cleaned: %s/%s'
        #    %(str(success_count),str(total_count)))

        self.initial_size = self.size()


    def summary(self):
        return {
            'name': self.name,
            'lib_dir':self.LIBDIR,
            'data_dir':self.DATADIR,
            'raw_data_tables': len(self),
            'company_count':len(self.get_ciks()),
            'quarters':self.quarter_array,
            'stmts': self.stmt_array,
            'cpu_load_factor': self.cpu_load_factor}

    def get_features(self):
        desc = '> Getting features (tags) Array'
        feature_arr = []
        for quarter,tag_df in tqdm(self.map.items(),desc = desc.ljust(40),ncols=85):
            if 'tag' in quarter: feature_arr += list(tag_df['tag'])
        return list(set(feature_arr))

    def size(self):
        count = 0 
        for item_df in self.map.values():
            count += item_df.shape[0]
        return count

    def shrink(self,ciks):
        print('> Shrinking Universe to optimize performance...')

        # Compute Size Before:
        
        before_count = self.size()
        for quarter in self.map.keys():
            if 'tag' not in quarter:
                # Construct pandas query 
                c_condition = self.map[quarter].cik == ciks[0]
                for ind,cik in enumerate(ciks):
                    if ind != 0:  c_condition = c_condition | self.map[quarter].cik == cik
                #print(self.map[quarter][c_condition])
                self.map[quarter].drop(self.map[quarter][c_condition].index, inplace=True)
        count_after = self.size()

        print(before_count - count_after)

        print('> Universe shrank by a factor of: %s'%(str(float(before_count/count_after))))
        print('> Universe is now %s percent of it\'s original size'%(str(100 * float(count_after/self.initial_size))))

    def get_tags(self):
        return self.get_features()

    def get_ciks(self):
        '''
            Gets unique ciks '''
        desc = '> Getting Cik Array'
        cik_arr = []
        for quarter,sub_df in self.map.items():
            if 'sub' in quarter: cik_arr += list(sub_df['cik'])
        return list(set(cik_arr))
