import pandas as pd
import os
import numpy as np

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download')

## read csv into memory, force pandas to read in mixed columns
bts_raw = pd.read_csv('billionton_state_download.csv', low_memory = False)

## only keep wastes, not cash crops
bts_raw = bts_raw[bts_raw['Production Unit'] == 'dt']

## columnar pivot table, with state index
bts_states = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'], columns = ['Scenario','Resource Category',  'Biomass Price'],
                              values = 'Production', aggfunc = np.sum)

## pivot table to match Tory data
bts_national = pd.pivot_table(bts_raw, index = ['Year','Feedstock'], columns = ['Scenario','Resource Category',  'Biomass Price'],
                              values = 'Production', aggfunc = np.sum)


bts_states.to_csv('bts_states_curves.csv')
bts_national.to_csv('bts_national_curves.csv')
