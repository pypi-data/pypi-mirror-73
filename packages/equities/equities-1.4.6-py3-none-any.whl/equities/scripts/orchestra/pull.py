import sys 
import os
import json
import psutil
import shutil 
from datetime import datetime
import time

import threading 
import multiprocessing

import pandas as pd 
import numpy  as np 

from tqdm import tqdm 
import emoji as emo

sys.path.append(os.path.join('lib'))
from equities.lib.pull.sec.Universe import Universe as Gu
from equities.lib.pull.sec.Company  import Company  as Gc
from equities.lib.pull.sec.waiter   import waiter   as Gw

from equities.lib.pull.yahoo.Universe import Universe as Yu
from equities.lib.pull.yahoo.Company  import Company  as Yc
from equities.lib.pull.yahoo.waiter   import waiter   as Yw 

#from pull.wikipedia.Universe import Universe as Wu
#from pull.wikipedia.Company  import Company  as Wc
#from pull.wikipedia.waiter   import waiter   as Ww 
#from pull.wikipedia.Company  import Company  as Wc

from equities.lib.access.DataAccessor import DataAccessor 

class pull(object):
    '''
    
    '''

    def __init__(self):

        # File and Data dirs
        self.FILEDIR = os.path.dirname(os.path.realpath(__file__))
        self.DATADIR = os.path.join(self.FILEDIR,'..','..','data')

        # Makes clean dir 
        self._mk_data_dirs()

        # Get ciks from data dir
        self.ciks = [elem for elem in os.listdir(os.path.join(self.DATADIR,'clean'))\
                          if elem != '.DS_Store']

        # Instantiate resolver for symbol resolution
        # Instantiates data accessor.
        self.da  = DataAccessor()  

        # Generate Initialization Manifest
        self.manifest   = None
        self.properties = None
        self.filter     = None

        # Data Config for yahoo and sec
        self.config = {
            'yahoo':
                {'stmts': ['income','balance','cash'],
                'freqs': ['annual','quarterly'],
                'ticks': [],
                'min_date': '2010-01-01',
                'max_date': datetime.today().strftime("%Y-%m-%d"),
                'call_threshold':10,
                'financial_statements':False,
                'pit_price':False,
                'ts_price':True,
                'summary':False,
                'statistics':True,
                'eps':False,
                'shares_outstanding':False,
                'av_shares_outstanding':False
                },
            'sec':
                {'quarter_start' : '2009q1',
                'quarter_end'    : '2020q2'
                },
            'wikipedia':
                {'company_names': [],
                'sentence_count': 10}   
            } 

        # Manifest residual items
        self.yahoo_items   = ['prices','dividends']
        self.sec_items = ['income','balance',
                              'cash','undefined',
                              'equity','header'] 

        # Maps that define, user input to csv file name conversions
        self.sec_map = {'income':'IS',
                            'balance':'BS',
                            'cash':'CF',
                            'undefined':'UN',
                            'equity':'EQ',
                            'header':'header'}

        self.ncols = 85

    def _mk_data_dirs(self):
        # Makes clean Directory
        for data_dir in ['clean','sec','yahoo']:
            if data_dir not in os.listdir(os.path.join(self.DATADIR)):
                os.mkdir(os.path.join(self.DATADIR,data_dir))

    def _mk_ticker_dirs(self,u):
        # Makes clean/cik Directories 
        if type(u) == type(Gu()):
            ciks = u.get_ciks()
        elif type(u) == type(Yu()):
            res_map = self.da.resolver.resolve(u.tickers,'ticker','cik')
            ciks = list(res_map.values())
        else:
            ciks = []
        for cik in ciks:
            if str(cik) not in os.listdir(os.path.join(self.DATADIR,'clean')):
                out_path = os.path.join(self.DATADIR,'clean',str(cik))
                os.mkdir(out_path)

    def _clean_dirs(self):
        self.update_manifest()
        clean_df = self.manifest[self.manifest.T.sum(axis = 0) == 0]
        cleanable_ciks = list(clean_df.index)
        for cik in cleanable_ciks:
            clean_path = os.path.join(self.DATADIR,'clean',str(cik))
            os.rmdir(clean_path)
        
        # Updates manifest.json
        self.update_manifest()
        # Updates properties.json
        self.update_properties()
        # Updates filter.json
        self.update_filter()
        # Updates merge.json
        self.update_merge()

    def _memory_halt(self,mem_lim = 0.05):

        mem = psutil.virtual_memory()
        mem_free = mem.available / mem.total 
        while mem_free <= mem_lim:
            print('\r> Memory Halt Triggered. Free Memory %s percent. Waiting for \
                memory to free up...'%(str(mem_free)),end = '')
            time.sleep(60)
            mem = psutil.virtual_memory()
            mem_free = mem.available / mem.total 
        
    def _sec_manifest(self):
        manifest_map = {}
        raw_dir = os.path.join(self.DATADIR,'clean')
        for cik in [x for x in os.listdir(raw_dir) if x != '.DS_Store']:
            cik_arr = []
            for item in self.sec_items:
                if self.sec_map[item]+'.csv' in os.listdir(os.path.join(raw_dir,str(cik))):
                    cik_arr.append(1)
                else:
                    cik_arr.append(0)
            manifest_map[cik] = cik_arr
        manifest_df = pd.DataFrame(manifest_map)
        manifest_df.index = pd.Index(self.sec_items)
        return manifest_df.T

    def _yahoo_manifest(self):
        ''' Generates Yahoo Manifest df '''
        manifest_map = {}
        raw_dir = os.path.join(self.DATADIR,'clean')
        for cik in [x for x in os.listdir(raw_dir) if x != '.DS_Store']:
            cik_arr = []
            for item in self.yahoo_items:
                if item+'.csv' in os.listdir(os.path.join(raw_dir,str(cik))):
                    cik_arr.append(1)
                else:
                    cik_arr.append(0)
            manifest_map[cik] = cik_arr
        manifest_df = pd.DataFrame(manifest_map)
        manifest_df.index = pd.Index(self.yahoo_items)
        return manifest_df.T

    def _sec_properties(self):
        ''' Generates Sec Properties df '''
        properties_map = {}
        properties_index = None
        for cik in self.manifest.index:
            try:
                # Load Header df
                in_path = os.path.join(self.DATADIR,'clean',str(cik),'header.csv') 
                header_df = pd.read_csv(in_path)
                header_df.replace({'':'date'}, inplace = True)
                header_df = header_df.T
                last_date = list(header_df.columns)[-1]
                properties_map[cik] = list(header_df[last_date])
                properties_index = header_df.index
            except Exception as e:
                print(e)
                properties_map[cik] = [None for i in range(len(properties_map[cik]))]
                pass
        properties_df = pd.DataFrame(properties_map)
        properties_df.index = properties_index
        return properties_df.T
    
    def _yahoo_properties(self):
        return pd.DataFrame()

    def _filter(self):
        # Default filter json
        filter_map = {}

        # Open properties.json
        properties_path = os.path.join(self.DATADIR,'..','lib','pull','properties.json')
        with open(properties_path) as f:
            try:
                properties_df = pd.DataFrame(json.load(f)).T
            except Exception as e:
                print(e)
                print("CRITICAL ERROR! could not find properites.json. quitting..")
                quit() 
        for prop in properties_df.columns:
            filter_map[prop] = list(set(list(properties_df[prop])))
        return filter_map


    def _merge(self):
        #Default merge json
        merge_map = {
            'feature_collapser':['pca','tag_reduce_2','drop_sparse_2'],
            'stmt_merge':['all']
        }
        return merge_map

    def execute_pipeline(self,test = False,multi_process = False,quarters = [],ciks=[]):
        total_stages = 12
        pipeline_str = lambda emoji,x,total : ' > %s  ( '\
        %(str(emo.emojize(emoji,use_aliases=True)))+str(x)+' )'

        #print('\n\n>>> STARTING EQUITIES DATA ACQUISITION')
        #print(pipeline_str(':rocket:','ordering data from the SEC',0).replace('-','='))
        #print(pipeline_str(':gun:','cleaning the pipelines',1))
        self.purge_pipeline()

        if quarters == []:
            quarters = \
                ['2019q4','2019q3','2019q2','2019q1',
                 '2018q4','2018q3','2018q2','2018q1',
                 '2017q4','2017q3','2017q2','2017q1',
                 '2016q4','2016q3','2016q2','2016q1',
                 '2015q4','2015q3','2015q2','2015q1',
                 '2014q4','2014q3','2014q2','2014q1',
                 '2013q4','2013q3','2013q2','2013q1',
                 '2012q4','2012q3','2012q2','2012q1',
                 '2011q4','2011q3','2011q2','2011q1']
        
        '''quarters = ['2019q4','2019q3','2019q2','2019q1']'''
                    #'2018q4','2018q3','2018q2','2018q1']
        gw = Gw(data_config = {'sec':self.config['sec']}) 
        #quarters = gw.quarter_array
        gw.download_data(quarters = quarters)                       

        #print(pipeline_str(':boom:','expanding universe',3))
        gu = Gu()
        gu.build()

        #print(pipeline_str(':memo:','saving data',4))
        if type(ciks) == type(int(0)):
            cik_arr = gu.get_ciks()[:ciks]
        elif type(ciks) == type([]):  
            cik_arr = ciks
        elif ciks == []:
            print("==>")
            cik_arr = gu.get_ciks()
        else:
            cik_arr = []
        self.dump_sec(gu,cik_arr,epoch = 10,multi_process=False)

        print(pipeline_str(':sweat_drops:','cleaning storage',12))
        self._clean_dirs()

        print('>>> complete...\n')

    def update_properties(self):
        # Generates and saves properties
        y = self._sec_properties()
        g = self._yahoo_properties()
        self.properties = pd.concat([y,g],axis = 1)

        # Prints updated properties
        #print('> Updating sec/properties.json. It has shape:\t\t %s'\
        #%(str(self.properties.shape)))

        # Saves properites as json
        out_path = os.path.join(self.DATADIR,'..','lib','pull','properties.json')
        self.properties.T.to_json(out_path,orient='columns')

    def update_manifest(self):
        # Generates and saves data manifest
        y = self._sec_manifest()
        g = self._yahoo_manifest()
        self.manifest = pd.concat([y,g],axis = 1)

        # Updates chef's ciks
        self.ciks = list(self.manifest.index)

        # Prints updated manifest
        #print('> Updating sec/manifest.json. It has shape:\t\t %s'\
        #%str(self.manifest.shape))

        # Saves manifest as json
        out_path = os.path.join(self.DATADIR,'..','lib','pull','manifest.json')
        self.manifest.T.to_json(out_path,orient='columns')

    def update_filter(self):
        # Generates maximal (default) filter
        self.filter = self._filter()
        
        # Prints updated maximal filter 
        #print('> Updating sec/filter.json. It has length:\t\t %s'\
        #%(str(len(self.filter))))

        # Saves Filter as json
        out_path = os.path.join(self.DATADIR,'..','lib','pull','filter.json')
        with open(out_path, 'w') as jf:
            json.dump(self.filter, jf)

    def update_merge(self):
        # Generates maximal (default) merge
        self.merge = self._merge()
        # Prints updated maximal filter 
        #print('> Updating sec/merge.json. It has length: \t\t %s'\
        #%(str(len(self.merge))))
        #print(self.filter)
        # Saves Filter as json
        out_path = os.path.join(self.DATADIR,'..','lib','pull','merge.json')
        with open(out_path, 'w') as jf:
            json.dump(self.merge, jf)

    def purge_pipeline(self,test = False):
        try: Gw().purge_data()
        except: print('No sec waiter to purge...'); pass
        try: Yw().purge_data()  
        except: pass #print('\t\t> No yahoo data to purge...'); pass
        # cleans 'clean' data directory
        clean_path = os.path.join(self.DATADIR,'clean')
        for cik in os.listdir(clean_path):
            try: shutil.rmtree(os.path.join(clean_path,cik))
            except: pass
        #print('>>> complete...')

    def dump_sec(self,u,ciks,epoch = 10,multi_process=False):
        desc = '\t\t> Dumping sec Data (multiprocess =%s)'%(str(multi_process))
        self._mk_ticker_dirs(u)

        pipeline_str = lambda emoji,x,total : ' > %s  ( '\
        %(str(emo.emojize(emoji,use_aliases=True)))+str(x)+' )'
        

        if multi_process:
            print(desc)
            process_map = {}
            # Define processes   
            desc_1 = '^ Processes are warming up. process_count: %s'%str(len(ciks)).ljust(40)
            for cik in tqdm(ciks,desc=desc_1,ncols=self.ncols):
                c = Gc(cik = cik, u = u)
                process_map['process_%s'%(cik)] = multiprocessing.Process(target = c.to_csv, args=(u,))
                process_map['process_%s'%(cik)].start()
                
                #self._memory_halt()
             # Continiues to Print active proccesses 
            time_start = datetime.now()
            while len(multiprocessing.active_children()) > 1:
                time.sleep(10)
                print('\r^ Processes currently active: %s   (Time Elapsed: %s)'%\
                (str(len(multiprocessing.active_children())),str(datetime.now()-time_start)),end = '')

            # Joining Process
            #desc_3 = '^ Processes are joining. '.ljust(40)
            #for process_name,process in tqdm(process_map.items(),desc = desc_3,ncols=self.ncols):
            #     process_map[process_name].join()
        
        else:
            to_remove_ciks = []
            for cik in tqdm(ciks,desc = pipeline_str(':memo:','saving dataframes',3),ncols=self.ncols):
                c = Gc(cik = cik, u = u)
                try:
                    to_remove_ciks.append(cik)
                    c.to_csv(u)
                except Exception as e:
                    print(e)

                '''
                if (ind % epoch == 0):
                    u.shrink(to_remove_ciks)
                    to_remove_ciks = []'''


    def dump_yahoo(self,u,tickers,multi_process = False):
        desc = '> Dumping Yahoo Data (multiprocess =%s)'%(str(multi_process))
        self._mk_ticker_dirs(u)
        if multi_process:
            print(desc)
            process_map = {}
            # Define process
            desc_1 = '^ Processes are warming up. process_count: %s'%str(len(tickers)).ljust(40)
            for ticker in tqdm(tickers,desc=desc_1,ncols=self.ncols):
                c = Yc(ticker = ticker, u = u)
                process_map['process_%s'%(ticker)] = \
                    multiprocessing.Process(target = c.to_csv,args=(u,self.da.resolver,))
                process_map[process_name].start()
                #self._memory_halt()
            
            # Continiues to Print active process 
            time_start = datetime.now()
            while len(multiprocessing.active_children()) > 1:###dee
                time.sleep(10)
                print('\r^ Processes currently active: %s (Time Elapsed: %s)'\
                %(str(len(multiprocessing.active_children())),str(datetime.now() - time_start)),end = '')
            
            # Joining process
            desc_3 = '^ Waiting for process to join.'.ljust(40)
            for process_name, process in tqdm(process_map.items(),desc = desc_3,ncols=self.ncols):
                process_map[process_name].join()
        else:
            for ticker in tqdm(tickers,desc = desc,ncols=self.ncols):
                c = Yc(ticker = ticker, u = u)
                try: c.to_csv(u,self.da.resolver)
                except Exception as e: pass #print(e)


    def dump_wikipedia(self,u):
        print('TODO')

if __name__ == '__main__':

    order = order()
    order.execute_pipeline(test = False,multi_process = False)



