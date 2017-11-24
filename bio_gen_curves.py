import pandas as pd
import os
import numpy as np

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download')

## read csv into memory, force pandas to read in mixed columns
bts_raw = pd.read_csv('billionton_state_download.csv', low_memory = False)

## only keep wastes, not cash crops
bts_raw = bts_raw[bts_raw['Production Unit'] == 'dt']

## Pathways category matching, taken from NYSERDA data spreadsheet
os.chdir(r'C:\Users\dan\Documents\BiofuelsDevelopment\bts-data\BTS-data')
mappings = pd.read_csv('feedstock_mappings.csv', index_col=0)


## bin conversion
bin_conversion_dict = pd.Series(mappings['E3conv_cat'].values,
                                index = mappings.index).to_dict()

def EthreeCat(feedstock):
    try:
        ethree = bin_conversion_dict[feedstock]
    except KeyError:
        ethree = 'NonPathways'
    return(ethree)

bts_raw['EthreeCategory'] = bts_raw['Feedstock'].apply(EthreeCat)

## columnar pivot table, with state index
bts_states = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory', 'Feedstock'],
                            columns = ['Scenario','Resource Category', 'Biomass Price'],
                            values = 'Production', aggfunc = np.sum)

## pivot table to match Tory data
bts_national = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory','Feedstock'],
                              columns = ['Scenario','Resource Category', 'Biomass Price'],
                              values = 'Production', aggfunc = np.sum)

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')

bts_states.to_csv('bts_states_bdtcurves.csv')
bts_national.to_csv('bts_national_bdtcurves.csv')
