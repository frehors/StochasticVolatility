import pandas as pd

def load_data():
    # sheet SPX options header in row 6
    close = 3094.04

    spx_options = pd.read_excel('data/Data20191113.xlsx', sheet_name='SPX options', header=5)
    spx_options['date'] = pd.to_datetime(spx_options['date'])
    spx_options['exdate'] = pd.to_datetime(spx_options['exdate'])
    spx_options['maturity'] = (spx_options['exdate'] - spx_options['date']).dt.days
    spx_options['strike_price'] = spx_options['strike_price'].astype(float) / 1000
    # remove options with no bid
    spx_options = spx_options[spx_options['best_bid'] > 0]
    # remove in the money options for both calls and puts
    spx_options = spx_options[((spx_options['strike_price'] > close) & (spx_options['cp_flag'] == 'C'))
                              | ((spx_options['strike_price'] < close) & (spx_options['cp_flag'] == 'P'))]

    return spx_options

df = load_data()
