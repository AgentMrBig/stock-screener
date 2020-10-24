import mplfinance as mpf
from pandas_datareader import data
df = data.DataReader("TSLA", 'yahoo', start="12-30-2019")
print(df.values)
mpf.plot(df, type='candle', ylabel = 'Price US$', title="TESLA Share price", volume=True, mav=(20,50), style='yahoo')