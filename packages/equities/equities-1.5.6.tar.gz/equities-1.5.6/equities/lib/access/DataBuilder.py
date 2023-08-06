import os 
import pathlib
import json

import pandas as pd
import numpy as np

from tqdm import tqdm 

'''
    Don't Worry too much about this file,
    Still in progress, A Tag Collapser effectively reduces 
    the number of features that we have. 

    Not important now...
'''

class DataBuilder(object):

    def __init__(self,request_config):

        self.filter_map  = request_config['filter']
        self.properties_map = request_config['properties']
        self.merge_map      = request_config['merge']

        # Directories
        try:self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except: self.LIBDIR = os.get_cwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','data')

        # Load Config
        self.config = {}
        for json_file in ['manifest.json','properties.json','filter.json','merge.json']:
            json_path = os.path.join(self.LIBDIR,'..','pull',json_file)
            with open(json_path, 'r') as jf:
                self.config[json_file.replace('.json','')] = json.load(jf)
 
        # Data accessor object 
        self.da = DataAccessor()
        self.ciks = self.da.ciks
        
        # Final Data 
        self.data = {}
        self.tags = []
    
    def apply_filter_map(self):
        print('Cik Count before Manifest Filter(s): %s'%(str(len(self.ciks))))
        dense_ciks = []
        for cik in self.ciks:
            add_cik = True
            for item,val in self.filter_map.items():
                if val and self.config['manifest'][str(cik)][item] == 0:
                    add_cik = False
            if add_cik: dense_ciks.append(cik)
        self.ciks = dense_ciks
        print('Cik Count after Manifest Filter(e): %s'%(str(len(self.ciks))))

    def apply_properties_map(self):
        print('Cik Count before Properties Filter(s): %s'%(str(len(self.ciks))))
        sieve_ciks = []
        for cik in self.ciks:
            add_cik = True
            for item,prop_arr in self.properties_map.items():
                    if self.config['properties'][str(cik)][item] not in prop_arr:
                        add_cik = False
            if add_cik: sieve_ciks.append(cik)
        self.ciks = sieve_ciks
        print('Cik Count after Properties Filter(e): %s'%(str(len(self.ciks))))

    def get_data(self):
        s_get = 0
        for cik in self.ciks:
            for item,val in self.filter_map.items():
                if val:
                    self.data[(cik,item)] = self.da.get(cik,item)
                    #print(self.data[(cik,item)]) 
                    s_get += 1
        total_data_items = int(len(self.ciks)*len(self.filter_map.keys()))
        print('Data for %s Ciks requested.'%(str(len(self.ciks))))
        print('Data item success count: %s/%s'%(str(s_get),str(total_data_items)))

    def get_tags(self):
        tag_array = []
        for cik_item,df in self.data.items():
            tag_array += list(df.index)
        self.tags = list(set(tag_array))
        print('Total tags in data: %s'%(str(len(self.tags))))

    def collapse_features(self):
        for (cik,item),df in self.data.items():
            # Apply Feature Collapsers (in order)
            for merge_item in self.merge_map['feature_collapser']:
                self.data[(cik,item)] = FeatureCollapser.apply(merge_item,df)

    def merge_data(self):
        merge_df = None
        if self.config['merge']['stmt_merge'] == 'add':
            merge_df = pd.concat(self.data.values(),axis = 1)
        self.data = merge_df

    def export_data(self,kind):
        if kind.lower() == 'csv':
            # Create Nivo Data Directory 
            if 'ds' in os.lsistdir(self.DATADIR):
                os.mkdir(os.path.join(self.DATADIR,'ds'))
            # Creates CIK directories in nivo directory 
            self.data.to_csv(os.path.join(self.DATADIR,'ds','exported_data.csv'))
        if kind.lower() == 'json_records':
            # Create Nivo Data Directory 
            if 'json_records' not in os.listdir(self.DATADIR):
                os.mkdir(os.path.join(self.DATADIR,'json_records'))
            # Creates CIK directories in nivo directory 
            NDir = os.path.join(self.DATADIR,'json_records')
            for cik in self.ciks:
                if cik != '.DS_Store' and cik not in os.listdir(os.path.join(NDir)):
                    os.mkdir(os.path.join(NDir,str(cik)))
            # Saves and transforms data
            desc = 'Transforming and Saving json data files'.ljust(40)
            for (cik,item),df in tqdm(self.data.items(),desc=desc,ncols=85):
                # sec transform
                if item in self.da.sec_items:
                    out_path = os.path.join(NDir,str(cik),item+'.json')
                    df.reset_index().to_json(out_path,orient = 'records')
            
    
    def build(self,kind):

        if kind.lower() == 'data_science' or kind.lower() == 'ds':
            total_stages = 7
            build_str = lambda x,total : '-'*150+'\n > Stage: %s/%s ( '\
            %(str(total),str(total_stages))+str(x)+' )\n'+'-'*115+'\n'

            print(build_str('> Starting DataBuilder build process. (kind = %s)'%(str(kind)).replace('-','='),0))
            print(build_str('> Applying manifest filter...',1))
            self.apply_filter_map()

            print(build_str('> Applying properties (sieve) filter...',2))
            self.apply_properties_map()

            print(build_str('> Getting data with DataAccessor() and manifest filter...',3))
            self.get_data()

            print(build_str('> Getting tags from self.data()...',4))
            self.get_tags()

            print(build_str('> Collapsing features...',5))
            self.collapse_features()

            print(build_str('> Merging data ...',6))
            self.merge_data()

            print(build_str('> Exporting data...',7))
            self.export_data('csv')

        elif kind.lower() == 'nivo_d3' or kind.lower() == 'nivo':
            total_stages = 7
            build_str = lambda x,total : '-'*150+'\n > Stage: %s/%s ( '\
            %(str(total),str(total_stages))+str(x)+' )\n'+'-'*150+'\n'

            print(build_str('> Starting DataBuilder build process. (kind = %s)'%(str(kind)),0))
            print(build_str('> Getting data with DataAccessor() and manifest filter...',1))
            self.get_data()

            print(build_str('> Exporting data...',2))
            self.export_data('json_records')