import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import load_data

# Data loading
spx, vix = load_data()

spx_calls = spx[spx['cp_flag'] == 'C'].drop(columns=['cp_flag', 'best_bid', 'best_offer', 'optionid'])
spx_calls = spx_calls.melt(id_vars=['exdate', 'strike_price'], value_vars = 'mid', value_name='price')
# load yield curve
yield_curve = pd.read_csv('tempYields.csv')
yield_curve['date'] = pd.to_datetime(yield_curve['date'])


vix_calls = vix[vix['cp_flag'] == 'C'].drop(columns=['cp_flag', 'best_bid', 'best_offer', 'optionid'])
vix_calls = vix_calls.melt(id_vars=['exdate', 'strike_price'], value_vars = 'mid', value_name='price')
vix_calls['exdate'] = pd.to_datetime(vix_calls['exdate'])

# Insert exdate from vix_calls into yield with nan values
yield_curve = yield_curve.set_index('date')
yield_curve = yield_curve.reindex(pd.date_range(start=yield_curve.index[0], end=yield_curve.index[-1], freq='D'))
yield_curve = yield_curve.reset_index()
yield_curve = yield_curve.rename(columns={'index': 'date'})
yield_curve['date'] = pd.to_datetime(yield_curve['date'])
# Interpolate yield curve forward fill
yield_curve['yield'] = yield_curve['yield'].interpolate(method='bfill')

# Merge yield curve with vix_calls
vix_calls = pd.merge(vix_calls, yield_curve, left_on='exdate', right_on='date', how='left')
vix_calls['yield'] = vix_calls['yield'].interpolate(method='bfill')
vix_calls = vix_calls.drop(columns=['date'])

#vix_calls = pd.merge(vix_calls, yield_curve, left_on='exdate', right_on='date')
#yield_curve = pd.merge(yield_curve, vix_calls, left_on='date', right_on='exdate', how='left')
#vix_calls = pd.merge(vix_calls, yield_curve, left_on='exdate', right_on='date', how='')

# interpolate yields for dates in vix_calls