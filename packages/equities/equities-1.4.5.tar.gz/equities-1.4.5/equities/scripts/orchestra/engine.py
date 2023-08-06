import sys 
import os 
import emoji as emo

from tqdm import tqdm

from equities.lib.engine.graph.secParser   import secParser 

class Engine(object):
    '''
        So because the engine is composed of many 
        submodules or parsers, for example 'graph' or 'core'
        The engine class itself contains other objects that 
        themselves have execute_pipeline() functions. 
        The engine only has an execute_pipeline() function 
        which calls all the relevant submodule execute_pipelines()
    '''

    def __init__(self):
        print('> Engine Instantiated.')

        self.Graph = graph()

    def execute_pipeline(self):

        self.Graph.purge_pipeline()
        self.Graph.execute_pipeline()


class graph(object):
    '''
        This is how we handle the Sec graph parser. 
        We can also add the wiki parser here. 
    '''

    def __init__(self):

        # File and Data dirs
        self.FILEDIR = os.path.dirname(os.path.realpath(__file__))
        self.DATADIR = os.path.join(self.FILEDIR,'..','..','data')

        # D3 JavaScript object array
        self.d3_nodes = []
        self.d3_links = []

        # meta
        self.ncols = 115

        self._mk_graph_dir()

    def _mk_graph_dir(self):
        if 'graph' not in os.listdir(self.DATADIR):
            os.mkdir(os.path.join(self.DATADIR,'graph'))

    def execute_pipeline(self):
        #print('>>> STARTING ARTEMIS NETWORK GRAPH GENERATION')

        # Printer Config 
        total_stages = 3
        pipeline_str = lambda emoji,x,total : '> %s  Stage: %s/%s ( '\
        %(str(emo.emojize(emoji,use_aliases=True)),str(total),str(total_stages))+str(x)+' )'
        print(pipeline_str(':rocket:','Initiated graph.execute_pipeline() - \
            constructing sector-company graph',0).replace('-','='))

        # Purges data directories
        print(pipeline_str(':gun:','Purging  Data Pipeline',1))
        self.purge_pipeline()

        # Instantiates graph parser
        print(pipeline_str(':boom:','Instantiating Graph Parser...',2))
        sgp = secParser()

        # Parse total market graph from downloaded data.
        print(pipeline_str(':runner:','Parsing Market Graph to data folder.',3))
        sgp.parse(kind = 'Market')

        # Parse sectors graphs from downloaded data.
        print(pipeline_str(':runner:','Parsing Divisions Graphs to data folder.',4))
        sgp.parse(kind = 'Divisions')

        print('>>> complete...\n')

    def purge_pipeline(self,test = False):
        # cleans 'clean' data directory
        desc = '> purging graph data... '
        for elem in tqdm(os.listdir(os.path.join(self.DATADIR,'graph')),\
            desc=desc,ncols=self.ncols):   
            try:    os.remove(os.path.join(self.DATADIR,'graph',elem))
            except Exception as e: print(e); pass

        
if __name__ == '__main__':

    graph = graph()
    graph.execute_pipeline()
