import os
import sys
import json
import argparse
import numpy as np
import multiprocessing
from typing import List
from contextlib import contextmanager

from hpogrid.components.defaults import *  

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)
        
def grid_site_setup():
    os.environ['ENABLE_HPOGRID_RUN'] = 'TRUE'
    os.environ['HPOGRID_DATA_DIR'] = kDataDir
    os.environ['HPOGRID_WORK_DIR'] = kWorkDir

def is_grid_job_running():
    return os.environ.get('ENABLE_HPOGRID_RUN', None)=='TRUE'

def get_base_path():
    if kHPOGridEnvPath not in os.environ:
        raise KeyError('{} environment variable not set.'
            'Try source setupenv.sh first.'.format(kHPOGridEnvPath))
    return os.environ[kHPOGridEnvPath]

def set_script_path(proj_name, undo=False):
    project_path = get_project_path(proj_name)
    script_path = os.path.join(project_path, 'scripts')
    
    if (script_path in sys.path) and (undo==True):
        sys.path.remove(script_path)
        os.environ["PYTHONPATH"].replace(script_path+":","")
        
    if (script_path not in sys.path) and (undo==False):
        sys.path.append(script_path)
        os.environ["PYTHONPATH"] = script_path + ":" + os.environ.get("PYTHONPATH", "")

def get_project_path(proj_name):
    if is_grid_job_running():
        proj_path = kDataDir
    else:
        base_path = get_base_path()
        proj_path = os.path.join(base_path, 'project', proj_name)
    if not os.path.exists(proj_path):
        raise RunTimeError('Project "{}" not found.'.format(proj_name))
    return proj_path

def get_config(proj_name, config_type):
    project_path = get_project_path(proj_name)
    config_name = kConfig2FileMap[config_type]
    confg_path = os.path.join(project_path, 'config', config_name)
    if not os.path.exists(confg_path):
        raise FileNotFoundError('Missing {} config file: {}'.format(
            config_type.replace('_',''), confg_path))
    with open(confg_path) as config_file:
        config = json.load(config_file)
    return config

def get_project_config(proj_name):
    return get_config(proj_name, config_type='project')

def get_hpo_config(proj_name):
    return get_config(proj_name, config_type='hpo')

def get_grid_config(proj_name):
    return get_config(proj_name, config_type='grid')    

def get_model_config(proj_name):
    return get_config(proj_name, config_type='model')    

def get_search_space_config(proj_name):
    return get_config(proj_name, config_type='search_space')    

@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

def get_physical_devices(device_type='GPU'):
    import tensorflow as tf
    physical_devices = tf.config.list_physical_devices('GPU')
    return physical_devices

def get_n_gpu():
    physical_devices = get_physical_devices('GPU')
    return len(physical_devices)

def get_n_cpu():
    return multiprocessing.cpu_count()


def extract_tarball(in_path:str, out_path:str) ->List[str]:
    tarfiles = [ f for f in os.listdir(in_path) if f.endswith('tar.gz')]
    extracted_files = []
    for f in tarfiles:
        tar = tarfile.open(f, "r:gz")
        print('untaring the file {}'.format(f))
        tar.extractall(path=out_path)
        extracted_files += tar.getnames()
        tar.close()
    return extracted_files

def remove_files(files:List[str]):
    for ds in self.input_ds:
        if os.path.isfile(ds):
            os.remove(ds)
        elif os.path.isdir(ds):
            shutil.rmtree(ds)        
