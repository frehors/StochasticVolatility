import pandas as pd
#if you get an error after executing the code, try adding below. pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2020, 1, 27)
SP500 = web.DataReader(['sp500'], 'fred', start, end)

# daily returns
SP500['daily_returns'] = SP500['sp500'].pct_change()
SP500['daily_returns'] = SP500['daily_returns'].fillna(0)
#plot
SP500['daily_returns'].plot()
# show
plt.savefig('images/daily_returns.png')
