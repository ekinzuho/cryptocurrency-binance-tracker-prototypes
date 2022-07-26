# Created at May 2022 by @traderekin on Twitter
# Quantitative Analysis tryouts

import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import pandas as pd

requestklines_spot = requests.get("https://api.binance.com/api/v3/klines",
                                  params=dict(symbol="ZILUSDT", interval="4h", limit="500"))
requestklines_spot_result = requestklines_spot.json()

dataframe_spot = pd.DataFrame(requestklines_spot_result,
                              columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                       "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                       "Taker Buy Quote Asset Volume", "Ignore"])
dataframe_spot["Volume"] = dataframe_spot["Volume"].astype(float)
# print(dataframe_spot)

requestklines_futures = requests.get("https://fapi.binance.com/fapi/v1/klines",
                                     params=dict(symbol="ZILUSDT", interval="4h", limit="500"))
requestklines_futures_result = requestklines_futures.json()

dataframe_futures = pd.DataFrame(requestklines_futures_result,
                                 columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                          "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                          "Taker Buy Quote Asset Volume", "Ignore"])
dataframe_futures["Volume"] = dataframe_futures["Volume"].astype(float)

#request_openInterest = requests.get("https://fapi.binance.com/futures/data/openInterestHist",
                                     #params=dict(symbol="SNXUSDT", period="5m", limit="500"))
#request_openInterest_result = request_openInterest.json()

# dataframe_openInterest = pd.DataFrame(request_openInterest_result, columns=["Symbol", "Open Interest", "Open Interest Value", "Time"])
#dataframe_openInterest = pd.DataFrame(request_openInterest_result)
#dataframe_openInterest_check = dataframe_openInterest.columns.values[1]
#print(dataframe_openInterest)

# fig = go.Figure(data=[
#    go.Candlestick(x=dataframe_spot['Open Time'], open=dataframe_spot['Open'], high=dataframe_spot['High'],
#                   low=dataframe_spot['Low'], close=dataframe_spot['Close'])])

fig = go.Figure(data=[
    go.Candlestick(x=dataframe_futures['Open Time'], open=dataframe_futures['Open'], high=dataframe_futures['High'],
                   low=dataframe_futures['Low'], close=dataframe_futures['Close'])])
fig.update_layout(xaxis_rangeslider_visible=False)
fig.show()

spotVol = dataframe_spot["Volume"]
perpVol = dataframe_futures["Volume"]
#spotVsPerpVol = (dataframe_spot["Volume"] / dataframe_futures["Volume"])
spotVsPerpVol = (dataframe_futures["Volume"] / dataframe_spot["Volume"])
#openInterest = dataframe_openInterest["sumOpenInterest"]

figure, axis = plt.subplots(3, 1)

axis[0].plot(spotVol)
axis[0].set_title("Spot Volume")
axis[1].plot(perpVol)
axis[1].set_title("Perp Volume")
axis[2].plot(spotVsPerpVol)
axis[2].set_title("Perp/Spot Volume")
#axis[3].plot(openInterest)
#axis[3].set_title("Open Interest")

plt.show()
