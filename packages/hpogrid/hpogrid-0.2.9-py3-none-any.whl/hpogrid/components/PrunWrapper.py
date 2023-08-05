import re
import os
import sys
import shutil
import atexit
import argparse
from pandatools.Group_argparse import GroupArgParser
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
import types
import json
import copy
from pandatools.MiscUtils import commands_get_output, commands_get_status_output
from pandatools import MiscUtils
    
    
from pandatools import Client
from pandatools import PsubUtils
from pandatools import AthenaUtils
from pandatools import PLogger



class PrunWrapper():
    def __init__(self):
        taskParamMap = {}
        taskParamMap['osInfo'] = PsubUtils.get_os_information()
    
    def to_json(self):
        pass
    
    def to_xml(self):
        pass



