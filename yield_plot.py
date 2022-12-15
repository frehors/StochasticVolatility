import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from data import load_data
from scipy import optimize
from div_yield import yield_div_error
# Data loading
print('Loading data...')
#index_spx, option_spx = functions.get_data_spx()
spx, vix = load_data()
##Global variables
T = spx.exdate.unique()
S = 3094.04  # check this
q = 0.01
r = 0.01 * np.ones(len(T))
start_guess = np.append(q, r)

bound = np.array([0, None])
bound = np.tile(bound, len(start_guess))
bound = bound.reshape(len(start_guess), 2)

# Data Preprocessing
# get (at most) 5 closest atm option pairs for each maturity
print('Data Preprocessing...')
n = 5
spx['abs_moneyness'] = np.abs(S - spx['strike_price'])
ntm_options = np.array([])
for expiry in T:
    ntm_call = spx[(spx['exdate'] == expiry) & (spx['cp_flag'] == 'C')].sort_values(
        ['abs_moneyness'], ascending=True)
    ntm_call = ntm_call.head(n)

    ntm_put = pd.merge(
        spx[(spx['exdate'] == expiry) & (spx['cp_flag'] == 'P')],
        ntm_call['strike_price'],
        on=['strike_price'],
        how='inner'
    )

    ntm_options = np.append(ntm_options, ntm_call['optionid'])
    ntm_options = np.append(ntm_options, ntm_put['optionid'])

ntm_options = spx[spx['optionid'].isin(ntm_options)]

print('Calibrating yield curve...')
# calibrate only to NTM options
calibration = optimize.minimize(
    yield_div_error,
    start_guess,
    args=(S, ntm_options,),
    method='Nelder-Mead',
    bounds=bound,
    options={'maxiter': 10 ** 4, 'maxfev': 10 ** 4}
)

q_calibrated = pd.DataFrame({'dividend_rate': calibration.x[0]}, index=[0])
r_calibrated = pd.DataFrame({
    'date': T,
    'yield': calibration.x[1:]
})
# add maturity to yield
r_calibrated['maturity'] = (
    (r_calibrated['date'] - r_calibrated['date'].min()) /
    np.timedelta64(1, 'D')
) / 365

print('Calibrated yield curve:', r_calibrated)
print('Calibrated dividend rate: ', q_calibrated)
# save calibrated yield curve and dividend rate
q_calibrated.to_csv('dividend_rate.csv', index=False)
r_calibrated.to_csv('yield_curve.csv', index=False)

print('Plotting...')
# plot yield curve and dividend rate
plt.plot(
    r_calibrated['date'],
    r_calibrated['yield'],
    label='yield',
    marker='o'
)
plt.plot(
    r_calibrated['date'],
    q_calibrated['dividend_rate'][0] * np.ones(len(r_calibrated['date'])),
    label='dividend rate',
    linestyle='dashed'
)
plt.xticks(rotation=45)
plt.legend()
# add header to plot
plt.title('Calibrated Yield Curve and Dividend Rate, 2019-11-13')
# Fix formatting and save
plt.tight_layout()
plt.savefig('yield_curve.png')
print('ALL DONE!')