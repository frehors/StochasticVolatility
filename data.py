import pandas as pd
import numpy as np

def load_data():
    # sheet SPX options header in row 6
    close_spx = 3094.04
    close_vix = 13
    spx_options = pd.read_excel('data/Data20191113.xlsx', sheet_name='SPX options', header=5)
    spx_options['date'] = pd.to_datetime(spx_options['date'])
    spx_options['exdate'] = pd.to_datetime(spx_options['exdate'])
    spx_options['maturity'] = (spx_options['exdate'] - spx_options['date']).dt.days / 365
    spx_options['strike_price'] = spx_options['strike_price'].astype(float) / 1000
    spx_options['mid'] = (spx_options['best_bid'] + spx_options['best_offer']) / 2
    # remove options with no bid
    #spx_options = spx_options[spx_options['best_bid'] > 0]
    #spx_options = spx_options[spx_options['volume'] > 0]
    # remove in the money options for both calls and puts
    #spx_options = spx_options[((spx_options['strike_price'] > close_spx) & (spx_options['cp_flag'] == 'C'))
    #                          | ((spx_options['strike_price'] < close_spx) & (spx_options['cp_flag'] == 'P'))]

    vix_options = pd.read_excel('data/Data20191113.xlsx', sheet_name='VIX options and futures', header=5)
    vix_options['date'] = pd.to_datetime(vix_options['date'])
    vix_options['exdate'] = pd.to_datetime(vix_options['exdate'])
    vix_options['maturity'] = (vix_options['exdate'] - vix_options['date']).dt.days / 365
    vix_options['strike_price'] = vix_options['strike_price'].astype(float) / 1000
    # remove options with no bid
    #vix_options = vix_options[vix_options['best_bid'] > 0]
    # remove in the money options for both calls and puts
    vix_options = vix_options[((vix_options['strike_price'] > close_vix) & (vix_options['cp_flag'] == 'C'))
                              | ((vix_options['strike_price'] < close_vix) & (vix_options['cp_flag'] == 'P'))]
    vix_options['mid'] = (vix_options['best_bid'] + vix_options['best_offer']) / 2

    try:
        spx.drop(columns=['Mid', 'Strike'])
    except:
        pass
    try:
        vix.drop(columns=['Mid', 'Strike'])
    except:
        pass

    return spx_options, vix_options


spx, vix = load_data()

if False:
    # spx melt to long format with index exdate and columns maturity and strike for calls
    spx_calls = spx[spx['cp_flag'] == 'C'].drop(columns=['cp_flag', 'best_bid', 'best_offer', 'optionid'])
    spx_calls = spx_calls.melt(id_vars=['exdate', 'strike_price'], value_vars = 'mid', value_name='price')
    # load yield curve
    yield_curve = pd.read_csv('yield_curve.csv')
    yield_curve['date'] = pd.to_datetime(yield_curve['date'])
    # merge
    spx_calls = pd.merge(spx_calls, yield_curve, left_on='exdate', right_on='date')
    spx_calls['maturity'] = (spx_calls['exdate'] - spx['date'].iloc[0]).dt.days / 365

    # set index to maturity and drop date and exdate
    spx_calls = spx_calls.set_index('maturity').drop(columns=['date', 'exdate', 'variable'])

    s0 = 3094.04
    # get int of days from datetime pandas series

# calculate RMSE between two columns

dat = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 2, 3]})
dat['rmse'] = np.sqrt(np.mean((dat['a'] - dat['b'])**2))



