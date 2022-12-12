import numpy as np
import pandas as pd
# put call parity


def put_call_parity(price, S, K, r, q, T, option_type):
    #Ensure compatility with numpy arrays

    if option_type in ('call', 'Call', 'CALL', 'c', 'C'):
        put_price = price - S*np.exp(-q*T) + K*np.exp(-r*T)
        return put_price
    call_price = price + S*np.exp(-q*T) - K * np.exp(-r* T)

    return call_price


def yield_div_error(param, S, dat):
    q = param[0]
    r = param[1:]

    df = pd.merge(
        dat[dat['cp_flag'] == 'P'][['exdate', 'strike_price', 'mid', 'date']],
        dat[dat['cp_flag'] == 'C'][['exdate', 'strike_price', 'mid']],
        on=['exdate', 'strike_price'],
        how='inner'
    )

    df = pd.merge(
        df,
        pd.DataFrame({'yield': r, 'exdate': dat.exdate.unique()}),
        on=['exdate'],
        how='inner'
    )

    df.rename(columns={'mid_x': 'mid_put', 'mid_y': 'mid_call'}, inplace=True)

    df['mid_put_parity'] = put_call_parity(
        df['mid_call'],
        S,
        df['strike_price'],
        df['yield'],
        q,
        ((df['exdate'] - df['date']) / np.timedelta64(1, 'D')) / 255,  # Annualize
        'call'
    )

    SE = np.sum((df['mid_put'] - df['mid_put_parity']) ** 2)

    return SE