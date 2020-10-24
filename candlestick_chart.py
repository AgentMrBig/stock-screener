import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

# Define time frame

start = dt.datetime(2010, 1, 1)
end = dt.datetime.now()

# Load Data
data = web.DataReader('TSLA', 'yahoo', start, end)

#print(data)

# Restructure Data
data = data[['Open', 'High', 'Low', 'Close']]

data.reset_index(inplace=True)
data['Date'] = data['Date'].map(mdates.date2num)

# Visualization

ax = plt.subplot()
ax.grid(True)
ax.set_title('TSLA Share Price', color='white')
ax.set_axisbelow(True)
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis_date()

candlestick_ohlc(ax, data.values, width=0.5, colorup='#00ff00')
plt.show()


print(data.head())