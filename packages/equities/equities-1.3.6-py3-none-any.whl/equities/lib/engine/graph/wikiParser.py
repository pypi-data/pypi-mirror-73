import os
import sys

import pandas as pd
import numpy as np

from tqdm import tqdm

class WikiParser(object):
    '''
        This class helps select relevant wikipedia links and sends them to clean 
        dir. 
    '''
    def __init__(self):

        # Get data and library directories.
        try :    self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except : self.LIBDIR  = os.getcwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','data','wikipedia')

        self.link_map = {}
        self.ncols    = 115

    def load_links(self):
        for link_csv in [x for x in os.listdir(os.path.join(self.DATADIR,'links')) if x!='.DS_Store']:
            link_df = pd.read_csv(os.path.join(self.DATADIR,'links',link_csv))
            self.link_map[link_csv.replace('_links.csv','')] = list(link_df['0'])

    def break_links(self):
        desc = '> breaking links'

        all_links,new_links = [],[]
        for link_arr in self.link_map.values():
            all_links += link_arr
        all_links = list(set(all_links))

        for link in tqdm(all_links,desc=desc,ncols=self.ncols): 
            count = 0
            for cik,link_arr in self.link_map.items():
                if link in link_arr:
                    count += 1
                if count >= 2:
                    new_links.append(link)
                    break

        for cik,link_arr in self.link_map.items():
            new_link_arr = []
            for link in link_arr:
                if link in new_links:
                    new_link_arr.append(link)
            self.link_map[cik] = new_link_arr

    def dump_raw_links(self):
        for link_csv in [x for x in os.listdir(os.path.join(self.DATADIR,'links')) if x!='.DS_Store']:
            link_df = pd.read_csv(os.path.join(self.DATADIR,'links',link_csv))
            link_df.write_csv(os.path.join(self.DATADIR,'..','clean',link_csv))
    
    """def parse_neighbour_graphs(self):


    def dump_neighbour_graphs(self)
    """

if __name__ == "__main__":

    lb = WikiParser()
    lb.load_links()
    lb.break_links()

    print(lb.link_map)

    #print(lb.link_map['1124212'])
