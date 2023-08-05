"""
    Module for formatting tables, texts and figures used in hpogrid
"""
from tabulate import tabulate
import pandas as pd
import yaml
import copy
from pdb import set_trace

kDefaultTableStyle = 'psql'
kDefaultStrAlign = 'left'

class ColorCode():
    RED = '\033[0;91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'


def yaml_nested_dict(data, depth=1, layer=0):
    data = copy.deepcopy(data)
    if layer < depth:
        layer += 1
        for d in data:
            if (layer == depth):
                if isinstance(data[d], dict):
                    data[d] = yaml.dump(data[d], allow_unicode=True,
                                       default_flow_style=False, sort_keys=False)
            else:
                data[d] = dict_to_yaml(data[d], depth, layer)
    return data

def create_table(data, columns=None, indexed=True, transpose=False,
    tableformat=kDefaultTableStyle, stralign=kDefaultStrAlign):

    df = pd.DataFrame(data, columns=columns)
    if transpose:
        df = df.transpose()
    table = tabulate(df, showindex=indexed, headers=df.columns, 
        tablefmt=tableformat,
        stralign=stralign)
    return table

def create_formatted_dict(data, columns=None, indexed=True, transpose=False,
    tableformat=kDefaultTableStyle, stralign=kDefaultStrAlign, yaml_depth=None):
    if yaml_depth:
        data = yaml_nested_dict(data, yaml_depth)
    return create_table(data.items(), columns, indexed, transpose, tableformat, stralign)

    
