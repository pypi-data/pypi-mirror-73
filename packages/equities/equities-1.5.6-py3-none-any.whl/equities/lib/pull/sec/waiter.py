from io import BytesIO, StringIO
import os
import sys
import requests
import shutil
import zipfile


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import emoji as emo
from tqdm import tqdm

class waiter(object):
    '''
        Description: This waiter


        The waiter library is a small class that handles our data
        feeds. In particular the waiter class allows you to download all raw
        data to equities/data/... Currently libraries using the waiter:
    '''

    def __init__(self,data_config = {}):

        default_config = {'sec':{'quarter_start':'2009q1','quarter_end':'2019q4'}}
        self.data_config = data_config if data_config != {} else default_config

        self.data_start_lim = self.data_config['sec']['quarter_start']
        self.data_end_lim   = self.data_config['sec']['quarter_end']
        # SEC Dataset base url
        self.BASEURL = 'https://www.sec.gov/files/dera/data/financial-statement-data-sets/'

        # Get data and library directories.
        try :    self.LIBDIR  = os.path.dirname(os.path.realpath(__file__))
        except : self.LIBDIR  = os.getcwd(); pass
        self.DATADIR = os.path.join(self.LIBDIR,'..','..','..','data','sec')

        # Generates list of possible quarters.
        self.quarter_array = self._generate_quarters()

        # Makes data directory structures.
        self._mk_dirs()

    def _mk_dirs(self):
        '''
            Makes necessary data directory structures for downloading
            data.  '''
        ''
        for dir in ['raw','clean']:
            if dir not in os.listdir(os.path.join(self.DATADIR)):
                os.mkdir(os.path.join(self.DATADIR,dir))

    def _generate_quarters(self):
        '''
            Computes an array of quarters between self.data_start_lim and
            self.data_end_lim.

            returns:
                quarter_array - array mentioned above. '''

        # Gets start and end years.
        start_year    = int(self.data_start_lim.split('q')[0])
        end_year      = int(self.data_end_lim.split('q')[0])

        # Constructs array of quarters.
        quarter_array = [str(year) + quarter\
                         for year    in range(start_year,end_year + 1)\
                         for quarter in ['q1','q2','q3','q4']]

        return quarter_array

    def download_data(self,
            quarters = []):

        '''
            Downloads sec data. Called by the download data method. '''
        # Computes quarters to download
        download_quarters = quarters if quarters != [] else self.quarter_array

        # Restricts testing quarters.
        #download_quarters = [year+quarter \
        #                     for year in ['2019']\
        #                     for quarter in ['q1','q2']]\
        #                     if test else download_quarters

        pipeline_str = lambda emoji,x,total : ' > %s  ( '\
        %(str(emo.emojize(emoji,use_aliases=True)))+str(x)+' )'

        # Iterates through quarter lists and downloads
        for download_quarter in tqdm(download_quarters,
                                     desc=pipeline_str(':package:','downloading packages',0),ncols=85):
            try:
                # Requests sec structured data
                r   = requests.get(self.BASEURL + download_quarter + '.zip', stream=True)

                # Instantiates zipfile
                z   = zipfile.ZipFile(BytesIO(r.content))

                # Extracts and saves to data directory
                z.extractall(os.path.join(self.DATADIR,'raw',download_quarter))
            except Exception as e:
                print('\n\n\nCould not get: %s, failed with exception: %s'%(str(download_quarter),str(e)))
                pass


    def purge_data(self,quarter_array = []):
        '''
            Deletes all data downloaded using the self.download_database()
            method.

            args:
                1) quarter_array - array of quarters to purge. If this
                   variable defaults to [], all quarters avaliable are
                   deleted.
        '''
        # Computes quartes to purge.
        purge_quarters = quarter_array \
        if quarter_array != [] \
        else os.listdir(os.path.join(self.DATADIR,'raw'))

        pipeline_str = lambda emoji,x,total : ' > %s  ( '\
        %(str(emo.emojize(emoji,use_aliases=True)))+str(x)+' )'

        # Trys to purge quarter directories.
        for purge_quarter in tqdm(purge_quarters,\
        desc = pipeline_str(':gun:','cleaning the pipelines',0),ncols=85):
            try: shutil.rmtree(os.path.join(self.DATADIR,'raw',purge_quarter))
            except: pass




