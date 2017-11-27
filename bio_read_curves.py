import pandas as pd
import os
import numpy as np  #delete if not used in deaccumlate

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')

## reads generated curves back as multi-index w/ scenario selection
class ParseCurves:
    '''class for bdt reading methods'''
    def __init__(self, file_type, path, scenario):
        self.file_type = file_type.lower()
        self.path = path
        self.scenario = scenario


    def read_bdt_curves(self):
        '''reads supply curve data as bdt'''
        if self.file_type == 'state':
            self.frame = pd.read_csv(self.path, index_col=[0,1,2], header = [0,1,2])
            self.frame = self.frame[self.scenario]
        elif self.file_type == 'national':
            self.frame = pd.read_csv(self.path, index_col = [0,1], header = [0,1,2])
            self.frame = self.frame[self.scenario]
        else:
            print('bad entry: enter state or national')
        return(self.frame)


    def read_energy_curves(self):
        if self.file_type == 'state':
            frame = pd.read_csv(self.path, index_col=[0,1,2,3], header = [0,1,2,3])
            #frame = frame[scenario]
        elif self.file_type == 'national':
            frame = pd.read_csv(self.path, index_col = [0,1,2], header = [0,1,2,3])
            #frame = frame[scenario]
        else:
            print('bad entry: enter state or national')
        return(frame)

    ## add method to slice to year/ scenario
    ## add method to deaccumulated once we figure that out...
