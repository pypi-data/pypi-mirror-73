import sys 
import os 
from os import system, name 
import time
from time import sleep 


import emoji as emo

from orchestra.env import env as AppEnv
from orchestra.pull import pull as DataPuller

# Import art engine. 
from orchestra.engine import Engine as ParseEngine 

FILE_PATH = os.path.dirname(os.path.realpath(__file__))

def play(build,ui = False):
    '''
        Play is the primary method for the conductor. 
        Use the build argument to specify what we want the 
        conductor to do. This defines a particular config. 
        A config is effectively a boolean valued map that 
        when passed into play determines which pipelines 
        we want to run. 

        Each script in the orchestra, has an object within similar 
        name. Each object contains an execute_pipeline() function. 

        I Feel like this file is pretty straight forward. 

    '''

    clear() # Clear stdout
    clear() # Clear stdout again
    
    broken_pipe_count = 0  # This keeps track of # of broken pipes. 
    broken_pipe_arr   = [] # If a pipe breaks we keep track of names here.

    # Gets build settings.
    # Take a look at these functions to see how these builds are defined.
    # Feel free to add other configs and builds if you think they are useful.
    if build == "lib_build" or "ui" in build:
        config = getLibBuildConfig(ui=ui)
    else: 
        print('Build %s not recognized... quitting...'%(str(build)))

    # 1. BUILD ENVIROMENT
    #  ie: Builds python and node enviroments
    try:
        if config['env']: AppEnv().execute_pipeline()
    except:
        broken_pipe_count+=1; broken_pipe_arr.append('env');pass

    # 2. PULL DATA
    #   ie: Download all required data and parse
    try:
        os.chdir(os.path.join(FILE_PATH))
        if config['pull']: DataPuller().execute_pipeline()
    except Exception as e:
        broken_pipe_count+=1; broken_pipe_arr.append(('pull',e));print(e);pass

    # 3. Executes engine.
    #   ie: Construct engine and calls sub pipeline executes.
    try:
        os.chdir(os.path.join(FILE_PATH))
        if config['engine']: ParseEngine().execute_pipeline()
    except Exception as e:
        broken_pipe_count+=1; broken_pipe_arr.append(('engine',e));pass


    # Generate Final Report of pipeline failures
    broken_pipe_str = getBrokenPipeStr(broken_pipe_arr)

    print('='*115 +'\n\n End Report:\n%s'%(str(broken_pipe_str)) + '\n' +'='*115)


def getLibBuildConfig(ui=True):
    b_map = {'Y':True,'N':False}
    print('='*115 + '\n'+' '*40+'Welcome to the equities-engine App Builder ' + '\n'+'='*115)
    if ui:
        print('\n\nPlease select from the options below.\nIndicate either Y or N for each field.\n')
        config = {
            'env':      b_map[input('\t:)\tset up enviroment: ')],
            'pull':     b_map[input('\t:)\tpull, structure and save pull data: ')],
            'engine':   b_map[input('\t:)\tparse local art data with the engine: ')],
            'populate':     b_map[input('\t:)\tpopulate initial art data to gcp firestore: ')],
            'transfer': b_map[input ('\t:)\ttransfer local art data to services: ')],
            }
    else:
        config = {
            'env': True,
            'pull':True,
            'engine':True,
            'populate':False,
            'transfer':False
            }
    time.sleep(1.2)
    print('\nOkay here\'s your request:\n\tart_req: (env=%s,pull=%s,engine=%s,populate=%s,transfer=%s)\n'\
        %(config['env'],config['pull'],config['populate'],config['engine'],config['transfer']))
    for count_down in [3,2,1]: print('\rStarting in %s seconds...'%(str(count_down)),end='');time.sleep(1)
    print('\n --- \n')
    return config
    

def getBrokenPipeStr(broken_pipe_arr):
    broken_pipe_str = '\t Oh no :( A few pipes broke during the build process: \n'
    if len(broken_pipe_arr) != 0:
        for ind,broken_pipe in enumerate(broken_pipe_arr):
            broken_pipe_str += '\n\t\t'+str(ind+1)+') '+str(broken_pipe[0]) +'-\t'+str(broken_pipe[1])
    else: 
        broken_pipe_str = '\t'*3 + str(emo.emojize(':fire:',use_aliases=True)) + \
            '  -  art app build complete with no pipeline leaks! Woot! Woot!\n' + '\t'*3 + \
            'You can now cd into service directories to run the front and backends.'
    return broken_pipe_str

  
# define our clear function 
def clear(): 
  
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 




if __name__ == "__main__":

    if 'ui' in sys.argv: ui = True
    else: ui = False

    print('ui:::')
    print(ui)

    if len(sys.argv) == 1:
        print('No command line arguments found! Please reference the readme in the top level you fool...')
    else:
        play(sys.argv[1],ui=ui)
