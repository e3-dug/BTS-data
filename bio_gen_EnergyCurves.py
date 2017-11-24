os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download')

## read csv into memory, force pandas to read in mixed columns
bts_raw = pd.read_csv('billionton_state_download.csv', low_memory = False)

## only keep wastes, not cash crops
bts_raw = bts_raw[bts_raw['Production Unit'] == 'dt']

## unit conversion mappings, derived from NYSERDA data spreadsheet
mappings = pd.read_csv('feedstock_mappings.csv', index_col=0)


## bin conversion
bin_conversion_dict = pd.Series(mappings['E3conv_cat'].values,
                                index = mappings['BTSfeedstock']).to_dict()

def EthreeCat(feedstock):
    try:
        ethree = bin_conversion_dict[feedstock]
    except KeyError:
        ethree = None
    return(ethree)

bts_raw['EthreeCategory'] = bts_raw['Feedstock'].apply(EthreeCat)

## energy conversion

highgge_conversion_dict = pd.Series(mappings['high_eff'].values,
                                    index = mappings.index).to_dict()
lowgge_conversion_dict = pd.Series(mappings['low_eff'].values,
                                   index = mappings.index).to_dict()

def ConvertGGE(x, low_high):
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
bts_raw['low_gge'] = bts_raw[['Feedstock', 'Production']].apply(lambda x: ConvertGGE(x,'low'), axis = 1)
bts_raw['high_gge'] = bts_raw[['Feedstock', 'Production']].apply(lambda x: ConvertGGE(x,'high'), axis = 1)

## conversion from NYSERDA spreadsheet
tbtu_gge = 0.129/ 1.055/ 1000000
bts_raw['low_tbtu'] = bts_raw['low_gge'] * tbtu_gge
bts_raw['high_tbtu'] = bts_raw['high_gge'] * tbtu_gge

## generate cumulative curves
## low gge, columnar pivot table, with state index
bts_states_lgge = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'],
                                 columns = ['Scenario','Resource Category',  'Biomass Price'],
                                 values = 'low_gge', aggfunc = np.sum)

## low gge, national, pivot table to match Tory data
bts_national_lgge = pd.pivot_table(bts_raw, index = ['Year','Feedstock'],
                                   columns = ['Scenario','Resource Category',  'Biomass Price'],
                                   values = 'low_gge', aggfunc = np.sum)

## low gge, columnar pivot table, with state index
bts_states_lgge = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'],
                                 columns = ['Scenario','Resource Category',  'Biomass Price'],
                                 values = 'low_gge', aggfunc = np.sum)

## low gge, national, pivot table to match Tory data
bts_national_lgge = pd.pivot_table(bts_raw, index = ['Year','Feedstock'],
                                   columns = ['Scenario','Resource Category',  'Biomass Price'],
                                   values = 'low_gge', aggfunc = np.sum)

## low Tbtu columnar pivot table, with state index
bts_states_lbtu = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'],
                                 columns = ['Scenario','Resource Category',  'Biomass Price'],
                                 values = 'low_tbtu', aggfunc = np.sum)

## low national Tbtu pivot table to match Tory data
bts_national_lbtu = pd.pivot_table(bts_raw, index = ['Year','Feedstock'],
                                   columns = ['Scenario','Resource Category',  'Biomass Price'],
                                   values = 'low_tbtu', aggfunc = np.sum)

## high Tbtu columnar pivot table, with state index
bts_states_hbtu = pd.pivot_table(bts_raw, index = ['State', 'Year','Feedstock'],
                                 columns = ['Scenario','Resource Category',  'Biomass Price'],
                                 values = 'high_tbtu', aggfunc = np.sum)

## high national pivot table to match Tory data
bts_national_hbtu = pd.pivot_table(bts_raw, index = ['Year','Feedstock'],
                                   columns = ['Scenario','Resource Category',  'Biomass Price'],
                                   values = 'high_tbtu', aggfunc = np.sum)

## save to curves folder
os.chdir(r'S:\ZacharySubins_Documents\NYSERDA 100%\BTS Data Download\curves')

to_write = [bts_states_lgge, bts_national_lgge, bts_states_hgge, bts_national_hgge,
           bts_states_lbtu, bts_national_lbtu, bts_states_hbtu, bts_national_hbtu]


names = ['bts_state_lgge.csv', 'bts_national_lgge.csv', 'bts_states_hgge.csv',
         'bts_national_hgge.csv', 'bts_states_lbtu.csv', 'bts_national_lbtu.csv',
         'bts_state_hbtu.csv', 'bts_national_hbtu.csv']


for i, j in zip(to_write, names):
    i.to_csv(j)
