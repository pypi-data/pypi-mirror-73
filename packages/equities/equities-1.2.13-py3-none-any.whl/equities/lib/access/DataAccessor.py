import os 
import pathlib
import json

import pandas as pd
import numpy as np

from tqdm import tqdm 

from equities.lib.access.Resolver import Resolver 
from equities.lib.access.TagCollapser import TagCollapser

class DataAccessor(object):

    def __init__(self,lim = 2):

        # Directories
        try:self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except: self.LIBDIR = os.get_cwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','data')
        self.PULLDIR = os.path.join(self.DATADIR,'..','lib','pull')

        # clean ciks
        self.ciks = [elem for elem in os.listdir(os.path.join(self.DATADIR,'clean')) if elem != '.DS_Store']

        self.yahoo_items   = ['prices','dividends']
        self.sec_items     = ['income','balance','cash','undefined','equity'] 
        self.meta_items    = ['manifest.json','properties.json','filter.json','merge.json']
        self.sec_map       = {'income':'IS','balance':'BS','cash':'CF','undefined':'UN','equity':'EQ'}

        # Ever Data Accessor Object also has a Resolver 
        self.resolver  = Resolver()
        self.collapser = TagCollapser(lim = lim)

    # Data Methods 

    def get(self, item = None, cik = None,collapse = False):
        # Gets Yahoo Data
        if item.lower() in self.yahoo_items:
            in_file = os.path.join(self.DATADIR,'clean',str(cik),item+'.csv')
            get_df = self._get_yahoo_df(in_file,item)
        # Gets sec Data
        elif item.lower() in self.sec_items:
            in_file = os.path.join(self.DATADIR,'clean',str(cik),self.sec_map[item]+'.csv')
            get_df = self._get_sec_df(in_file,item)
        elif item.lower() == 'manifest':
            get_df = self._get_manifest_df(os.path.join(self.PULLDIR,'manifest.json'))
        elif item.lower() == 'properties':
            get_df = self._get_manifest_df(os.path.join(self.PULLDIR,'properties.json'))
        elif item.lower() == 'filter':
            get_df = self._get_manifest_df(os.path.join(self.PULLDIR,'filter.json'))
        elif item.lower() == 'merge':
            get_df = self._get_manifest_df(os.path.join(self.PULLDIR,'merge.json'))
        elif item.lower() == 'summary':
            try: 
                with open(os.path.join(self.DATADIR,'clean',str(cik),'summary.txt'),'r') as f:
                    return str(f.read())
            except: 
                return "";
        elif item.lower() == 'links':
            try:
                with open(os.path.join(self.DATADIR,'clean',str(cik),'links.txt')) as f:
                    return [line.rstrip() for line in f]
            except:
                return [];
        else:
            print('Get statement: Not recognized by ds.DataAccesor.get(%s,%s)'%(str(cik),str(item)))

        # Collapse if selected
        #print(self.collapser.tags_catalogued)
        if (self.collapser.tags_catalogued == False) and collapse:
            self.collapser.catalogue_tags()
        
        if collapse: 
            get_df = get_df.T
            get_df.index   = self.collapser.apply_cluster_transform(get_df.index)
            get_df['tags'] = get_df.index; get_df.reset_index(drop = True)
            get_df = get_df.groupby('tags').sum().T
        return get_df


    def _get_yahoo_df(self,in_file,item):
        item_name = item.replace('.csv','')
        yahoo_df = pd.read_csv(in_file)
        yahoo_df.rename({'formatted_date':item_name},axis = 1,inplace = True)
        yahoo_df.set_index(item_name,inplace = True)
        return yahoo_df

    def _get_sec_df(self,in_file,item):
        item_name = item.replace('.csv','')
        sec_df = df = pd.read_csv(in_file)
        sec_df.rename({'Unnamed: 0':item_name},axis = 1,inplace = True)
        sec_df.set_index(item_name,inplace = True)
        return sec_df.T

    # Pull Methods 

    def _get_manifest_df(self,in_file):
        return pd.read_json(in_file)

    def _get_properties_df(self,in_file):
        return pd.read_json(in_file)

    def _get_merge_df(self,in_file,item):
        with open('./merge.json','r') as jf:
            merge_map = json.load(jf)
        max_selection = 0
        for label,selection in merge_map.items():
            if len(selection) > max_selection:
                max_selection = len(selection)
        for label,selection in merge_map.items():
            for null_index in range(max_selection - len(selection)):
                merge_map[label].append('nan')
        return pd.DataFrame(merge_map)

    def _get_filter_df(self,in_file,item):
        with open('./merge.json','r') as jf:
            filter_map = json.load(jf)
        max_selection = 0
        for label,selection in filter_map.items():
            if len(selection) > max_selection:
                max_selection = len(selection)
        for label,selection in filter_map.items():
            for null_index in range(max_selection - len(selection)):
                filter_map[label].append('nan')
        return pd.DataFrame(filter_map)



if __name__ == '__main__':

    da = DataAccessor()
    #print(da.get(item = 'income', cik = '73756',collapse=False).shape)
    #print(da.get(item = 'income', cik = '73756',collapse=True).shape)
    