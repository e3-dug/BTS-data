import pandas as pd
import os
import numpy as np

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')

## reads generated curves back as multi-index w/ scenario selection
def read_curves(file_type, path, scenario = ['3% yield inc.', 'High housing, high energy demands', 'Wastes and other residues']):
    '''Reads csv output as pandas MultiIndex.
    User provides file national or state file type, path and scenario
    '''
    if file_type == 'state':
        frame = pd.read_csv(path, index_col=[0,1,2,3], header = [0,1,2])
        frame = frame[scenario]
    elif file_type == 'national':
        frame = pd.read_csv(path, index_col = [0,1,2], header = [0,1,2])
        frame = frame[scenario]
    else:
        print('bad scenario entry: enter state or national')
    return(frame)
