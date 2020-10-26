# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 23:31:02 2020

@author: Eric Hendrix
"""

import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import mplfinance as mpf
import finnhub
plt.style.use('bmh')

# 'global' variables needed
# use your own api key https://finnhub.io/ its free
FINNHUB_CLIENT = finnhub.Client(api_key="bu76jmf48v6rajd4sij0")
US30 = 'OANDA:US30_USD'
GBPUSD = 'OANDA:GBP_USD'
XAUUSD = 'OANDA:XAU_USD'
EURUSD = 'OANDA:EUR_USD'
USDJPY = 'OANDA:USD_JPY'
candles = ''
df = ''


# This function takes a date string in format 'Dec 25, 2018' and
# returns a timestamp for that date string
def setTime(time):
    # Convert strings to datetime.datetime
    time_obj = datetime.strptime(time, '%b %d, %Y')
    # Convert datetime.datetime to timestamp
    time_stamp = datetime.timestamp(time_obj)
    # next I remove the dec by converting from float to int
    time_stamp = int(time_stamp)
    return time_stamp


def getFinanceData(fromTime, toTime, symbol, period):
    # api call to https://finnhub.io/ getting daily stock candles for netflix
    # in a specified date range
    #nflxData = finnhub_client.stock_candles('nflx', 'D', fromTime_stamp, toTime_stamp)

    # api call to get forex candles
    candles = FINNHUB_CLIENT.forex_candles(symbol, period, fromTime, toTime)
    # print(candles)

    # Forex symbols
    print(candles)

    # pandas dataframe
    df = pd.DataFrame(candles)
    return df

# Supported resolution includes 1, 5, 15, 30, 60, D, W, M .Some timeframes might not be available depending on the exchange.
df = getFinanceData(setTime('Dec 25, 2018'),
                    setTime('Oct 25, 2020'), US30, '60')


# def plotData():
    # Visualize the close price data
    # string indeces for data
    # 0=c, 1=h, 2=l, 3=0, 4=s, 5=t, 6=v
    # plt.figure(figsize=(16,8))
    # plt.title('US30')
    # plt.xlabel('Days')
    # plt.ylabel('Close Price USD')
    # plt.plot(df['c'])
    # plt.show()

    # mpf.plot(df, type='candle', ylabel = 'Price US$', title="US30", volume=True, mav=(20,50), style='yahoo')

def predictPrices(model, dataframe, visualize):
    # Get close price
    df = dataframe[['c']]
    future_days = 25
    prediction_days1 = 5
    prediction_days2 = 10

    # Create a new column (target) shifted 'x' units/days up
    df['Prediction'] = df[['c']].shift(-future_days)

    # Create the feature data set (x) and convert it to a numpy array and remove the
    # last 'x' rows/days
    X = np.array(df.drop(['Prediction'], 1))[:-future_days]

    # Create the target data set (y) and convert it to a numpy array and get all the
    # target values except the last 'x' rows/days
    Y = np.array(df['Prediction'])[:-future_days]

    # TEST idea here is to create predictions that we can use for actual future
    # TEST Create dataset (XP) and convert it to numpy array
    XP = np.array(df.drop(['Prediction'], 1))
    # TEST Create dataset (XP) and convert it to numpy array
    YP = np.array(df['Prediction'])  # [:+prediction_days1]

    # Split the data into 75% training and 25% testing
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.25)
    #x_train, x_test, y_train, y_test = train_test_split(XP,YP,test_size = 0.25)

    # Create the models
    # Create the decision tree regressor model
    tree = DecisionTreeRegressor().fit(x_train, y_train)

    # Create the linear regression model
    lr = LinearRegression().fit(x_train, y_train)

    # Get the last 'x' rows of the feature data set
    x_future = df.drop(['Prediction'], 1)[-future_days:]
    x_future = x_future.tail(future_days)
    x_future = np.array(x_future)

    tree_prediction = tree.predict(x_future)
    lr_prediction = lr.predict(x_future)

    # score the model
    print('Prediction Score, 1.0 being "perfect" ', lr.score(x_test, y_test))

    if visualize == 'false':
        if model == 'tree':
            # Show the model tree prediction
            print('Decision tree predictions ', tree_prediction)
        elif model == 'lr':
            # Show the model linear regression prediction
            print('Linear regression predictions ', lr_prediction)

    elif visualize == 'true':
        if model == 'tree':
            # Visualize the data
            predictions = tree_prediction

            valid = df[X.shape[0]:]
            valid['Predictions'] = predictions
            plt.figure(figsize=(16, 8))
            plt.title('US30 Model')
            plt.xlabel('Days')
            plt.ylabel('Close Price USD ($)')
            plt.plot(df['c'])
            plt.plot(valid[['c', 'Predictions']])
            plt.legend(['Orig', 'Val', 'Pred'])
            plt.show()
        elif model == 'lr':
            # Visualize the data
            predictions = lr_prediction

            valid = df[X.shape[0]:]
            valid['Predictions'] = predictions
            plt.figure(figsize=(25, 15))
            plt.title('US30 Model')
            plt.xlabel('Days')
            plt.ylabel('Close Price USD ($)')
            plt.plot(df['c'])
            plt.plot(valid[['c', 'Predictions']])
            plt.legend(['Orig', 'Val', 'Pred'])
            plt.show()

            # mpf.plot(df, type='candle', ylabel = 'Price US$', title="US30", volume=True, mav=(20,50), style='yahoo')
            # mpf.plot(valid[['c', 'Predictions']], type='candle', ylabel = 'Price US$', title="US30", volume=True, mav=(20,50), style='yahoo')


predictPrices('lr', df, 'true')
