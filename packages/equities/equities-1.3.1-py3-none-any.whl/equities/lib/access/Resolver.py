import os
import requests

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from tqdm import tqdm 

class Resolver(object):

    """
        The Resolver class in the symbols library resolves symbols. So
        our data sources have their own labelling system for their data,
        that is to say their own mapping schemes. We will eventually need
        to go from one map to another. The Resolver should be thought of
        as the inbetween between different symbols.

        Feel free to add your own mappings. Just follow the design pattern.

    """

    def __init__(self):

        try: self.FILEDIR = os.path.dirname(os.path.realpath(__file__))
        except: self.FILEDIR = os.getcwd();pass
        self.DATADIR = os.path.join(self.FILEDIR,'..','..','data','symbols')
    
        # Download Resolver data if it does not exist
        if 'cik_api.csv' not in os.listdir(os.path.join(self.DATADIR)):
            self._download_resolver_data(kind = 'cik_api')

        #self.cik_api_df    = self.parse_cik_api_df()
        #self.division_df   = self.parse_division_df()
        #self.industry_df   = self.parse_industry_df()
        #self.majorgroup_df = self.parse_majorgroup_df()
        #self.sic_df        = self.parse_sic_df()


    def _download_resolver_data(self,kind):
        if kind.lower() =='cik_api':
            '''
            exchanges,exchange_df_arr  = ['NYSE','NASDAQ','NYSE MKT','OTC'],[]
            for exchange in tqdm(exchanges,'Downloading Resolver Data for: %s...'%str(kind)):
                r = requests.get('https://mapping-api.herokuapp.com/exchange/%s'%(exchange))
                if exchange == '':
                    print(r.content)
                mapping_df = pd.DataFrame(r.json())
                #mapping_df.set_index('cik',inplace = True)
                exchange_df_arr.append(mapping_df)
            df = pd.concat(exchange_df_arr,axis = 0)'''
            r = requests.get('https://mapping-api.herokuapp.com/ticker/%5E')
            df = pd.DataFrame(r.json())
            #print(df.shape)
            out_path = os.path.join(self.DATADIR,'cik_api.csv')
            df.to_csv(out_path)

            # Need to add github download and parse for division,industry and majorgroup.

    ''' Parsing Resolver Data Functions '''
    def parse_cik_api_df(self):
        #cik_api_df = 
        #cik_api_df['sic'] = cik_api_df['sic'].apply(int)
        return pd.read_csv(os.path.join(self.DATADIR,'cik_api.csv'))
    def parse_division_df(self):
        return pd.read_csv(os.path.join(self.DATADIR,'divisions.csv'))
    def parse_industry_df(self):
         return pd.read_csv(os.path.join(self.DATADIR,'industry-groups.csv'))
    def parse_majorgroup_df(self):
         return pd.read_csv(os.path.join(self.DATADIR,'major-groups.csv'))
    def parse_sic_df(self):
        return pd.read_csv(os.path.join(self.DATADIR,'sic-codes.csv'))

    ''' Mapping Resolver Functions '''
    def mappify(self,df,x_label,y_label):
        return dict(zip(list(df[x_label]),list(df[y_label])))
        #print(m)
        #return m

    def _invert(self,map):
        return {v:k for k,v in map.items()}

    # Resolve Function
    def resolve(self,origin,x_label,y_label):
        #cik_api_map = self.cik_api_map(x_label=x_label,y_label=y_label)
        resolver_selector = lambda df,x_label,y_label : \
            (x_label in df.columns) and (y_label in df.columns) 
        if resolver_selector(self.cik_api_df,x_label,y_label):
            data_map = self.mappify(self.cik_api_df,x_label,y_label)
        elif resolver_selector(self.division_df,x_label,y_label):
            data_map = self.mappify(self.division_df,x_label,y_label)
        elif resolver_selector(self.industry_df,x_label,y_label):
            data_map = self.mappify(self.industry_df,x_label,y_label)
        elif resolver_selector(self.majorgroup_df,x_label,y_label):
            data_map = self.mappify(self.majorgroup_df,x_label,y_label)
        elif resolver_selector(self.sic_df,x_label,y_label):
            data_map = self.mappify(self.sic_df,x_label,y_label)
        else: 
            print('Error Bad resolution!... quitting...'); quit()
        #print(data_map)
        if type(origin) == type([]):
            resolve_map = {}
            s_count,f_count = 0,0
            for elem in origin:
                try:
                    resolve_map[elem] = data_map[elem]
                    s_count += 1
                except Exception as e:
                    #print(str(e))
                    f_count += 1 
            print('> Resolution report: Success Count: %s || Fail Count: %s '
            %(str(s_count),str(f_count)))
            return resolve_map
        else:
            return data_map[origin]

if __name__ == '__main__':

    # Download Data 
    Resolver()._download_resolver_data('cik_api')