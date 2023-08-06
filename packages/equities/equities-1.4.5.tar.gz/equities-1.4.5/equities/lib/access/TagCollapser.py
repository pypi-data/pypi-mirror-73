import os 
import pathlib
import json
import codecs

import pandas as pd
import numpy as np

from tqdm import tqdm 

'''
    Don't Worry too much about this file,
    Still in progress, A Tag Collapser effectively reduces 
    the number of features that we have. 

    Not important now...
'''



class TagCollapser(object):

    def __init__(self,lim):
        try:    self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except: self.LIBDIR  = os.get_cwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','data')
        self.PULLDIR = os.path.join(self.DATADIR,'..','lib','pull')
        self.ncols = 115
        self.lim = lim

        self.tags_catalogued = False

    def catalogue_tags(self):
        self.tags = self.collect_tags()
        self.clusters = self._compute_tag_clusters()
        self.cluster_map = self._compute_cluster_map()
        self.tags_catalogued = True

    def collect_tags(self):
        desc = '> Tag Collapser: Collecting Tags...'
        tags = []
        for quarter in tqdm([e for e in os.listdir(os.path.join(self.DATADIR,'sec','raw')) if e!='.DS_Store'],desc,ncols = self.ncols):
            file_path = os.path.join(self.DATADIR,'sec','raw',quarter,'tag.txt')
            with codecs.open(file_path,'r',encoding='utf-8',errors='ignore') as f:
                tag_df = pd.read_table(f,
                sep             = '\t',
                lineterminator  = '\n',
                engine          = 'c',
                error_bad_lines = True,
                warn_bad_lines  = True,
                low_memory      = False,
                memory_map      = True)
                tags = tags + list(tag_df['tag'])
        tags = [str(x) for x in list(set(tags))]
        tags.sort(reverse = True)
        return tags

    def _camel_case_split(self,str):
        start_idx = [i for i, e in enumerate(str) 
                 if e.isupper()] + [len(str)] 
  
        start_idx = [0] + start_idx 
        return [str[x: y] for x, y in zip(start_idx, start_idx[1:])]  

    def _str_shave(self,tag,lim):
        camel_case_arr = self._camel_case_split(tag)
        return ''.join(camel_case_arr[:lim])

    def _compute_tag_clusters(self):
        desc = '> Computing tag clusters'
        clusters = []
        for ind,tag in enumerate(tqdm(self.tags,desc=desc,ncols=self.ncols)):
            if ind == 0:
                cluster = []
                cluster.append(str(tag))
            else:
                if self._str_shave(str(self.tags[ind-1]),self.lim) == self._str_shave(str(tag),self.lim):
                    cluster.append(str(tag))
                else:
                    clusters.append(cluster)
                    cluster = []
                    cluster.append(str(tag))
        return clusters

    def _compute_cluster_map(self):
        cluster_map = {}
        for cluster in self.clusters:
            cluster_representative = cluster[0]
            for tag in cluster:
                cluster_map[tag] = cluster_representative
        return cluster_map


    def apply_cluster_transform(self,tags):
        #print(self.cluster_map)
        transformed_tags = []
        f_count = 0
        for tag in tags:
            try:
                transformed_tags.append(self.cluster_map[tag])
            except Exception as e:
                #print(e)
                f_count += 1
                transformed_tags.append(tag)
                pass
        print('> Transform Complete: Ratio: %s/%s'%(str(len(tags)- f_count),str(len(tags))))
        return transformed_tags


if __name__ == '__main__':
    tc = TagCollapser(lim = 2)
    print(len(tc.tags))
    tc.apply_cluster_transform()
    print(len(tc.tags))


    