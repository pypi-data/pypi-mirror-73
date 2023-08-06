import sys
import os 

import emoji as emo
import time

class env(object):

    def __init__(self):

        self.DIR = os.path.dirname(os.path.realpath(__file__))
        
        # Core Enviroment Directories 
        self.ARTEMISDIR  = os.path.join(self.DIR,'..','..')
        self.serverDIR   = os.path.join(self.ARTEMISDIR,'..','services','server')
        self.clientDIR   = os.path.join(self.ARTEMISDIR,'..','services','client')

    def python_env(self):
        '''
        Installs requirements and installs art as a package.
        
        '''
        os.chdir(self.ARTEMISDIR)
        os.popen('pip3 install -r requirements.txt')
        os.popen('python3 setup.py install')
    
    def service_env(self,service_dir,name):
        ''' 
        Calls npm install in service directory
        
        :service_dir: - os path to service dir.
        :name:        - str service name (client, server etc..)
        
        '''

        os.chdir(service_dir)

        if 'node_modules' not in os.listdir(service_dir):

            yarn_version = os.popen('yarn info run').read().split(' ')[2]

            if yarn_version[0] == 'v':
                #print('System has yarn installed. Art will use yarn \
                #    to install %s node modules.'%(name))
                print('> [%s] yarn %s install'%(name,yarn_version))
                os.popen('yarn install'); #print(stream.read())
            else:
                #print('System does not have yarn installed. Art will use\
                #     npm to install %s node modules.'%(name))
                print('> [%s] npm install'%(name))
                os.popen('npm install');  #print(stream.read())

        else: 
            print('> %s node modules already installed.'%(name))


    def execute_pipeline(self):
        '''
            Execute Pipeline

        '''
        print('>>> STARTING ARTEMIS ENVIROMENT SETUP')
        
        # Printer 
        total_stages = 3
        pipeline_str = lambda emoji,x,total : '> %s  Stage: %s/%s ( '\
        %(str(emo.emojize(emoji,use_aliases=True)),str(total),str(total_stages))+str(x)+' )'
        print(pipeline_str(':rocket:','Initiated env.execute_pipeline() - \
            Creating Artemis enviroments',0).replace('-','='))

        #print(pipeline_str(':snake:','Setting up python enviroment',1))
        #self.python_env()

        print(pipeline_str(':sailboat:','Installing client node modules',3))
        self.service_env(self.clientDIR,'client')

        print('>>> complete...')
        os.chdir(self.DIR)


if __name__ == '__main__':

    ENV = env()
    ENV.execute_pipeline()