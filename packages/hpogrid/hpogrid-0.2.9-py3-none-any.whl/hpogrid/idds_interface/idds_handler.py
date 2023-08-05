import os
import sys
import glob
import argparse
import json
from typing import Optional

from hpogrid.components.defaults import *
from hpogrid.utils import helper, stylus

class iDDSHandler():
    def __init__(self):

        # submit grid job via hpogrid executable
        if len(sys.argv) > 1:
            self.run_parser()

    def get_parser(self):
        parser = argparse.ArgumentParser(
                    formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument('proj_name', help='the project to submit a grid job')               
        parser.add_argument('-s','--site', help='site to submit the job to '
            '(this will override the grid config site setting)', choices=kGPUGridSiteList)
        return parser

    def run_parser(self):
        parser = self.get_parser()
        if os.path.basename(sys.argv[0]) == 'hpogrid':
            args = parser.parse_args(sys.argv[2:])
        else:
            args = parser.parse_args(sys.argv[1:])
        iDDSHandler.submit_job(args.proj_name, args.site)
        
    @staticmethod
    def submit_job(project_name:str, site:Optional[str]=None):
        grid_config = helper.get_project_config(project_name)['grid_config']
        project_path = helper.get_project_path(project_name)
        idds_config_path = os.path.join(project_path, 'idds', kiDDSConfigName)
        idds_search_space_path = os.path.join(project_path, 'idds', kiDDSSearchSpaceName)
        options = {}
        options['loadJson'] = idds_config_path 
        options['searchSpaceFile'] = idds_search_space_path
        if not site:
            site = grid_config['site']
        if (site != 'ANY'):
            options['site'] = site
        
        out_ds = grid_config['outDS']
        if '{HPO_PROJECT_NAME}' in out_ds:
            out_ds = out_ds.format(HPO_PROJECT_NAME=project_name)
        options['outDS'] = out_ds

        command = stylus.join_options(options)
        os.system("phpo {}".format(command))
        
        
        
        
        
        
        
        
        
        
        
        