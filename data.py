import pandas as pd


def load_data():
    # sheet SPX options header in row 6
    close_spx = 3094.04
    close_vix = 13
    spx_options = pd.read_excel('data/Data20191113.xlsx', sheet_name='SPX options', header=5)
    spx_options['date'] = pd.to_datetime(spx_options['date'])
    spx_options['exdate'] = pd.to_datetime(spx_options['exdate'])
    spx_options['maturity'] = (spx_options['exdate'] - spx_options['date']).dt.days
    spx_options['strike_price'] = spx_options['strike_price'].astype(float) / 1000
    # remove options with no bid
    spx_options = spx_options[spx_options['best_bid'] > 0]
    # remove in the money options for both calls and puts
    spx_options = spx_options[((spx_options['strike_price'] > close_spx) & (spx_options['cp_flag'] == 'C'))
                              | ((spx_options['strike_price'] < close_spx) & (spx_options['cp_flag'] == 'P'))]

    vix_options = pd.read_excel('data/Data20191113.xlsx', sheet_name='VIX options and futures', header=5)
    vix_options['date'] = pd.to_datetime(vix_options['date'])
    vix_options['exdate'] = pd.to_datetime(vix_options['exdate'])
    vix_options['maturity'] = (vix_options['exdate'] - vix_options['date']).dt.days
    vix_options['strike_price'] = vix_options['strike_price'].astype(float) / 1000
    # remove options with no bid
    vix_options = vix_options[vix_options['best_bid'] > 0]
    # remove in the money options for both calls and puts
    vix_options = vix_options[((vix_options['strike_price'] > close_vix) & (vix_options['cp_flag'] == 'C'))
                              | ((vix_options['strike_price'] < close_vix) & (vix_options['cp_flag'] == 'P'))]

    return spx_options, vix_options


spx, vix = load_data()
