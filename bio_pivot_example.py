import pandas as pd
import os
import numpy as np

## bone dry tonnes per tonne
bdt_t = 0.85

## bushels corn per tonne
bu_t = 39.3862

## pounds per tonne
lb_t = 2204.62

## from Doug's spreadsheet
bdt_conversions = {'Barley' : 0.0308,
                   'Corn' : 0.0237,
                   'Oats' : 0.0275,
                   'Sorghum' : 0.0241,
                   'Soybeans' : 0.0241, ## copied from Sorgum
                   'Wheat' : 0.0389}



'''
Converts feekstocks to bdt
probably not right
'''

def converter(row):
    if row['Production Unit'] == 'dt':
        return(row['Production'])
    elif row['Production Unit'] == 'lb':
        return(row['Production'] / lb_t * bdt_t)
    elif row['Production Unit'] == 'bu':
        return(row['Production'] * bdt_conversions[row['Feedstock']])
    else:
        return(None)

bts_raw['Production_bdt'] = bts_raw.apply(converter, axis = 1)

## columnar pivot table
bts_national = pd.pivot_table(bts_raw, index = ['Year'], columns = ['Scenario','Resource Category', 'Feedstock', 'Biomass Price'],
                              values = 'Production_bdt', aggfunc = np.sum)

scenario_select = ['3% yield inc.', 'High housing, high energy demands',
                  'Wastes and other residues']

bts_curves = bts_national[scenario_select]
