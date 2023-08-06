import os
import sys
import json
import random
import numpy as np
import pandas as pd
import networkx as nx

from tqdm import tqdm

from equities.lib.access.DataAccessor import DataAccessor as da 
from equities.objects                 import Company

class secParser(object):

    def __init__(self):

        self.LIBPATH = os.path.dirname(os.path.realpath(__file__))
        try: self.DATADIR    = os.path.join(self.LIBPATH,'..','..','..','data')
        except: self.DATADIR = os.getcwd()

        self.d3_nodes = []
        self.d3_links = []
        self.da       = da()

        # encodes labels of DataAccessor sic_df into ints
        
        self.encode_map     = {elem : 10000 +ind for ind,elem in enumerate('ABCDEFGHIJ')}
        self.inv_encode_map = {v:k for k,v in self.encode_map.items()}
        self.da.resolver.sic_df.replace(self.encode_map,inplace = True)

        self.market_id = 9999999
        self.ncols = 115

        # SIC Color map
        self.sic_cmap        = self._generate_color_map('SIC')
        self.majorgroup_cmap = self._generate_color_map('Major Group')
        self.industry_cmap   = self._generate_color_map('Industry Group')
        self.division_cmap   = self._generate_color_map('Division')

        #print(self.da.resolver.sic_df.columns)
        #self.majorgroup_cmap = self


    def _generate_random_color(self):
        number_of_colors = 1
        color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
             for i in range(number_of_colors)]
        return color[0]
    
    def _generate_color_map(self,column):
        color_map = {}
        sics = np.unique(self.da.resolver.sic_df[column])
        for sic in sics:
            color_map[sic] = self._generate_random_color()
        return color_map
    
    def _parse_full_market(self):
        
        #print('> Paring graph of type: market')

        self.d3_nodes = []
        self.d3_links = []

        # Get Unique Node Types
        node_map = lambda column : list(np.unique(self.da.resolver.sic_df[column]))
        divisions      = node_map('Division')
        majorgroups    = node_map('Major Group')
        industrygroups = node_map('Industry Group') 
        sics           = node_map('SIC')
        market         = ['Market']
         
        # Adds all nodes
        for ind,node in enumerate(divisions+majorgroups+industrygroups+sics):
            if node in divisions:
                tag   = 'Division'
                size  = 40 
                color =  self.division_cmap[node]
            elif node in majorgroups:
                tag   = 'Major Group'
                size  = 20
                color = self.majorgroup_cmap[node]
            elif node in industrygroups:
                tag   = 'Industry Group'
                size  = 10
                color = self.industry_cmap[node]
            elif node in sics:
                tag   = 'SIC'
                size  = 5
                color = self.sic_cmap[node]
            try:
                resolution_node = self.da.resolver.resolve(node,tag,'Description')
            except:
                encode_map_inv  = {v:k for k,v in self.encode_map.items()}
                resolution_node = encode_map_inv[node]
            self.d3_nodes.append({
                'id'  : int(node),
                'name': resolution_node,
                '_color' : color,
                '_size': int(size)
            })
        # Adds Market Node
        self.d3_nodes.append({
                'id'  : int(self.market_id),
                'name': 'Market',
                '_color' : '#fffacd',
                '_size': int(60)
            })

        # Adds Division edge cycle
        cycle_edges = []
        for ind,division in enumerate(divisions):
            self.d3_links.append({
                'tid': int(self.market_id),#res_id_map[target_resolution], 
                'sid': int(divisions[ind]) #res_id_map[source_resolution],
            })

        #Adds Graph Edges
        links = []
        for ind,row in self.da.resolver.sic_df.iterrows():
            # Add Division -> Major Group
            division_majorgroup_link = (row['Division'],row['Major Group'])
            if division_majorgroup_link not in links: links.append(division_majorgroup_link)

            # Add Major Group -> Industry Group
            majorgroup_industrygroup_link = (row['Major Group'],row['Industry Group'])
            if majorgroup_industrygroup_link not in links: links.append(majorgroup_industrygroup_link)

            # Add Industry Group -> SIC
            industrygroup_sic_link = (row['Industry Group'],row['SIC'])
            if industrygroup_sic_link not in links: links.append(industrygroup_sic_link)
            #print(len(links))

        # Convert Links to json
        for link in links:
            self.d3_links.append({
                    'tid': int(link[0]),
                    'sid': int(link[1])
                })

        # Dump Graph
        with open(os.path.join(self.DATADIR,'graph','division_nodes.json'), 'w+') as gf:
            json.dump(self.d3_nodes, gf) #print('> dumped: d3_nodes')
        with open(os.path.join(self.DATADIR,'graph','division_links.json'), 'w+') as gf:
            json.dump(self.d3_links, gf) #; print('> dumped: d3_link')

        print('> graph dumped with %s nodes and %s edges'\
            %(str(len(self.d3_nodes)),str(len(self.d3_links))))




    def _parse_full_polygon(self):
        
        #print('> Parsing graph of type: polygon')

        self.d3_nodes = []
        self.d3_links = []

        # Get Unique Node Types
        node_map = lambda column : list(np.unique(self.da.resolver.sic_df[column]))
        divisions      = node_map('Division')
        majorgroups    = node_map('Major Group')
        industrygroups = node_map('Industry Group') 
        sics           = node_map('SIC')
         
        # Adds all nodes
        for ind,node in enumerate(divisions+majorgroups+industrygroups+sics):
            if node in divisions:
                tag   = 'Division'
                size  = 40 
                color =  '#aa00b'
            elif node in majorgroups:
                tag   = 'Major Group'
                size  = 20
                color = '#2f4f4f'
            elif node in industrygroups:
                tag   = 'Industry Group'
                size  = 10
                color = '#ffe4e1'
            elif node in sics:
                tag   = 'SIC'
                size  = 5
                color = '#fffacd'
            try:
                resolution_node = self.da.resolver.resolve(node,tag,'Description')
            except:
                encode_map_inv  = {v:k for k,v in self.encode_map.items()}
                resolution_node = encode_map_inv[node]
            self.d3_nodes.append({
                'id'  : int(node),
                'name': resolution_node,
                '_color' : color,
                '_size': int(size)
            })

        # Adds Division edge cycle
        cycle_edges = []
        for ind,division in enumerate(divisions):
            if ind != len(divisions) - 1:
                self.d3_links.append({
                    'tid': int(divisions[ind]),#res_id_map[target_resolution], 
                    'sid': int(divisions[ind + 1]) #res_id_map[source_resolution],
                })
                cycle_edges.append((divisions,divisions[ind + 1]))
            else:
                self.d3_links.append({
                    'tid': int(divisions[ind]),
                    'sid': int(divisions[0])
                })

        #Adds Graph Edges
        links = []
        for ind,row in self.da.resolver.sic_df.iterrows():
            # Add Division -> Major Group
            division_majorgroup_link = (row['Division'],row['Major Group'])
            if division_majorgroup_link not in links: links.append(division_majorgroup_link)

            # Add Major Group -> Industry Group
            majorgroup_industrygroup_link = (row['Major Group'],row['Industry Group'])
            if majorgroup_industrygroup_link not in links: links.append(majorgroup_industrygroup_link)

            # Add Industry Group -> SIC
            industrygroup_sic_link = (row['Industry Group'],row['SIC'])
            if industrygroup_sic_link not in links: links.append(industrygroup_sic_link)
            #print(len(links))

        # Convert Links to json
        for link in links:
            self.d3_links.append({
                    'tid': int(link[0]),
                    'sid': int(link[1])
                })

        # Dump Graph
        with open(os.path.join(self.DATADIR,'graph','division_nodes.json'), 'w+') as gf:
            json.dump(self.d3_nodes, gf); print('> dumped: d3_nodes')
        with open(os.path.join(self.DATADIR,'graph','division_links.json'), 'w+') as gf:
            json.dump(self.d3_links, gf); print('> dumped: d3_link')

        print('> graph dumped with %s nodes and %s edges'\
            %(str(len(self.d3_nodes)),str(len(self.d3_links))))


    def _parse_divisions(self):

        #print('> Parsing divisions graphs')
        # Get Unique Node Types
        node_map = lambda column : list(np.unique(self.da.resolver.sic_df[column]))
        divisions      = node_map('Division')
        
        for division in divisions:

            self.d3_nodes = []
            self.d3_links = []
            division_df = self.da.resolver.sic_df[self.da.resolver.sic_df['Division'] == division]
            division_map = lambda column: list(np.unique(division_df[column]))

            majorgroups    = division_map('Major Group')
            industrygroups = division_map('Industry Group') 
            sics           = division_map('SIC')
            
            # Adds all nodes
            for ind,node in enumerate([division]+majorgroups+industrygroups+sics):
                if node in divisions:
                    tag   = 'Division'
                    size  = 50 
                    color =  self.division_cmap[node]
                elif node in majorgroups:
                    tag   = 'Major Group'
                    size  = 40
                    color = self.majorgroup_cmap[node]
                elif node in industrygroups:
                    tag   = 'Industry Group'
                    size  = 20
                    color = self.industry_cmap[node]
                elif node in sics:
                    tag   = 'SIC'
                    size  = 10
                    color = self.sic_cmap[node]
                try:
                    resolution_node = self.da.resolver.resolve(node,tag,'Description')
                except:
                    encode_map_inv  = {v:k for k,v in self.encode_map.items()}
                    resolution_node = encode_map_inv[node]
                self.d3_nodes.append({
                    'id'  : int(node),
                    'name': resolution_node,
                    '_color' : color,
                    '_size': int(size)
                })

            #Adds Graph Edges
            links = []
            for ind,row in self.da.resolver.sic_df.iterrows():
                if row['Division'] == division:
                    # Add Division -> Major Group
                    division_majorgroup_link = (row['Division'],row['Major Group'])
                    if division_majorgroup_link not in links: links.append(division_majorgroup_link)

                    # Add Major Group -> Industry Group
                    majorgroup_industrygroup_link = (row['Major Group'],row['Industry Group'])
                    if majorgroup_industrygroup_link not in links: links.append(majorgroup_industrygroup_link)

                    # Add Industry Group -> SIC
                    industrygroup_sic_link = (row['Industry Group'],row['SIC'])
                    if industrygroup_sic_link not in links: links.append(industrygroup_sic_link)
                    #print(len(links))

            # Convert Links to json
            for link in links:
                self.d3_links.append({
                        'tid': int(link[0]),
                        'sid': int(link[1])
                    })

            # Attach Company to SIC Links 
            division_name = str(self.da.resolver.resolve(self.inv_encode_map[division],'Division','Description')).replace(',','').replace(' ','_')
            desc = '> Adding companies to division %s graph'%(division_name)
            prop_df = self.da.get(item = 'properties')
            prop_len = len(prop_df.columns)
            f_count = 0
            for cik in tqdm(prop_df.columns,desc=desc,ncols=self.ncols):
                try: 
                    c = Company(cik = cik)
                    if int(division) == int(self.encode_map[c.division]):      
                        if str(c.sic)[-1] != '0':             
                            self.d3_nodes.append({
                                'id'  : int(cik) * 10000000000,
                                'name': c.name,
                                '_color' : self.sic_cmap[node],
                                '_size': int(10)
                            })
                            self.d3_links.append({ 
                                'tid': int(c.sic),
                                'sid': int(cik) * 10000000000
                            })
                            #print('**')
                        else:
                            #print('&&')
                            self.d3_nodes.append({
                            'id'  : int(cik) * 100000,
                            'name': c.name,
                            '_color' : self.industry_cmap[str(node)[:-1]],
                            '_size': int(10)
                            })
                            self.d3_links.append({ 
                                'tid': int(c.industry),
                                'sid': int(cik) * 100000
                            })
                except Exception as e:
                    f_count += 1
                    #print(str(e) + '--')
                    pass
                    
            #print('> Attached %s/%s companies to division: %s'%(str(prop_len-f_count),str(prop_len),str(division) ) )

            # Dump Graph
            division_name = str(self.da.resolver.resolve(self.inv_encode_map[division],'Division','Description')).replace(',','').replace(' ','_')
            with open(os.path.join(self.DATADIR,'graph',division_name+'_division_nodes.json'), 'w+') as gf:
                json.dump(self.d3_nodes, gf); #print('> dumped: d3_nodes')
            with open(os.path.join(self.DATADIR,'graph',division_name+'_division_links.json'), 'w+') as gf:
                json.dump(self.d3_links, gf); #print('> dumped: d3_link')

            desc = '> graph %s dumped with %s nodes and %s edges'\
                %(division_name,str(len(self.d3_nodes)),str(len(self.d3_links)))

    def parse(self,kind = 'polygon'):
        if kind.lower() == 'polygon':
            self._parse_full_polygon()
        elif kind.lower() == 'market':
            self._parse_full_market()
        elif kind.lower() == 'divisions':
            self._parse_divisions()
        else: 
            print('kind: %s - invalid argument'%(str(kind)))
    

if __name__ == "__main__":
    gp = Parser()
    gp._parse_divisions()
    
    