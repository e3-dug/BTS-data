import pandas as pd
import os
import numpy as np

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download')

## read csv into memory, force pandas to read in mixed columns
bts_raw = pd.read_csv('billionton_state_download.csv', low_memory = False)

## only keep wastes, not cash crops
bts_raw = bts_raw[bts_raw['Production Unit'] == 'dt']

## columnar pivot table, to match example from Tory
bts_national = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'], columns = ['Scenario','Resource Category',  'Biomass Price'],
                              values = 'Production', aggfunc = np.sum)

## select cases
scenario_select = ['3% yield inc.', 'High housing, high energy demands',
                  'Wastes and other residues']

bts_high = bts_national[scenario_select]

## drop unncessary level from MultiIndex
bts_high.columns = bts_high.columns.droplevel()

bts_high.to_csv('bts_piv.csv')
