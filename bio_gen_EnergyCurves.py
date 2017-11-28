import pandas as pd
import os
import numpy as np

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download')

## read csv into memory, force pandas to read in mixed columns
bts_raw = pd.read_csv('billionton_state_download.csv', low_memory = False)

## only keep wastes, not cash crops
bts_raw = bts_raw[bts_raw['Production Unit'] == 'dt']

## unit conversion mappings, derived from NYSERDA data spreadsheet
os.chdir(r'C:\Users\dan\Documents\BiofuelsDevelopment\bts-data\BTS-data')
mappings = pd.read_csv('feedstock_mappings.csv', index_col=0)


## bin conversion
bin_conversion_dict = pd.Series(mappings['E3conv_cat'].values,
                                index = mappings.index).to_dict()

def ethree_cat_ene(feedstock):
    try:
        ethree = bin_conversion_dict[feedstock]
    except KeyError:
        ethree = None
    return(ethree)


bts_raw['EthreeCategory'] = bts_raw['Feedstock'].apply(ethree_cat_ene)

## energy conversion

highgge_conversion_dict = pd.Series(mappings['high_eff'].values,
                                    index = mappings.index).to_dict()
lowgge_conversion_dict = pd.Series(mappings['low_eff'].values,
                                   index = mappings.index).to_dict()

def convert_gge(x, low_high):
    if low_high == 'low':
        try:
            gge_cal = lowgge_conversion_dict[x['Feedstock']] * x['Production']
            return(gge_cal)
        except KeyError:
            return(None)
    else:
        try:
            gge_cal = highgge_conversion_dict[x['Feedstock']] * x['Production']
            return(gge_cal)
        except KeyError:
            return(None)


## conversion efficiencies from NYSERDA spreadsheet
bts_raw['low_gge'] = bts_raw[['Feedstock', 'Production']].apply(lambda x: convert_gge(x,'low'), axis = 1)
bts_raw['high_gge'] = bts_raw[['Feedstock', 'Production']].apply(lambda x: convert_gge(x,'high'), axis = 1)

## conversion from NYSERDA spreadsheet
tbtu_gge = 0.129/ 1.055/ 1000000
bts_raw['low_tbtu'] = bts_raw['low_gge'] * tbtu_gge
bts_raw['high_tbtu'] = bts_raw['high_gge'] * tbtu_gge

os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')

## generate supply curves for low/high conversion pathways
def gen_curve(val_type, level):
    '''generates biomass supply curves from Billion ton study data
    returns ouptputs for 'gge' and 'tbtu' for low and high conversion pathways
    '''

    if val_type.lower() == 'gge':
        val = ['low_gge', 'high_gge']

    elif val_type.lower() == 'tbtu':
        val = ['low_tbtu', 'high_tbtu']

    else:
        raise ValueError('entry must be gge or tbtu')

    if level.lower() == 'state':
        out = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory' ,'Feedstock'],
                             columns = ['Scenario', 'Resource Category',  'Biomass Price'],
                             values = val, aggfunc = np.sum)

        return(out.to_csv('bts_' + str(val_type) + '_' + str(level) + '.csv'))

    elif level.lower() == 'national':
        out = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory' ,'Feedstock'],
                             columns = ['Scenario', 'Resource Category',  'Biomass Price'],
                             values = val, aggfunc = np.sum)

        return(out.to_csv('bts_' + str(val_type) + '_' + str(level) + '.csv'))

    else:
        print('invalide entry: enter state or national as level')


gen_curve('tbtu', 'state')
gen_curve('tbtu', 'national')
gen_curve('gge', 'state')
gen_curve('gge', 'national')


#vals = ['low_gge', 'high_gge', 'low_tbtu', 'high_tbtu']
#
#for i in vals:
#    gen_curve(i, 'national')
#    gen_curve(i, 'state')


#
#
#
# ## generate cumulative curves
# ## low gge, columnar pivot table, with state index
# bts_states_lgge = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory' ,'Feedstock'],
#                                  columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                  values = 'low_gge', aggfunc = np.sum)
#
# ## low gge, national, pivot table to match Tory data
# bts_national_lgge = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory','Feedstock'],
#                                    columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                    values = 'low_gge', aggfunc = np.sum)
#
# ## low gge, columnar pivot table, with state index
# bts_states_hgge = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory' ,'Feedstock'],
#                                  columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                  values = 'high_gge', aggfunc = np.sum)
#
# ## low gge, national, pivot table to match Tory data
# bts_national_hgge = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory','Feedstock'],
#                                    columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                    values = 'high_gge', aggfunc = np.sum)
#
# ## low Tbtu columnar pivot table, with state index
# bts_states_lbtu = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory' ,'Feedstock'],
#                                  columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                  values = 'low_tbtu', aggfunc = np.sum)
#
# ## low national Tbtu pivot table to match Tory data
# bts_national_lbtu = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory','Feedstock'],
#                                    columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                    values = 'low_tbtu', aggfunc = np.sum)
#
# ## high Tbtu columnar pivot table, with state index
# bts_states_hbtu = pd.pivot_table(bts_raw, index = ['State', 'Year', 'EthreeCategory' ,'Feedstock'],
#                                  columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                  values = 'high_tbtu', aggfunc = np.sum)
#
# ## high national pivot table to match Tory data
# bts_national_hbtu = pd.pivot_table(bts_raw, index = ['Year', 'EthreeCategory','Feedstock'],
#                                    columns = ['Scenario','Resource Category',  'Biomass Price'],
#                                    values = 'high_tbtu', aggfunc = np.sum)
#
# ## save to curves folder
# os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')
#
# to_write = [bts_states_lgge, bts_national_lgge, bts_states_hgge, bts_national_hgge,
#            bts_states_lbtu, bts_national_lbtu, bts_states_hbtu, bts_national_hbtu]
#
#
# names = ['bts_state_lgge.csv', 'bts_national_lgge.csv', 'bts_states_hgge.csv',
#          'bts_national_hgge.csv', 'bts_states_lbtu.csv', 'bts_national_lbtu.csv',
#          'bts_state_hbtu.csv', 'bts_national_hbtu.csv']
#
#
# for i, j in zip(to_write, names):
#     i.to_csv(j)
