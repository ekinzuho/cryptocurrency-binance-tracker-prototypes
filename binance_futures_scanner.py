# Created at July 2022 by @ekinco on Twitter
# Quantitative Analysis tryouts
import binance.client
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import pandas as pd
import binance.client as BClient
import websocket
import json

# Importing Binance api and api secret keys
f = open("binance_api_key.txt", "r")
binance_api_key = f.read()
f.close()
f = open("binance_secret_key.txt", "r")
binance_secret_key = f.read()
f.close()

client = BClient.Client(api_key=binance_api_key, api_secret=binance_secret_key)
"""
tickers = client.get_all_tickers()
"""

########################################################################################################################
########################################################################################################################
# This part creates a filtered list of PERPETUAL and USDT pairs to utilize in scanning

exchange_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
exchange = exchange_info.json()
exchange_symbols = exchange["symbols"]
ticker_list = []
for ex in exchange_symbols:
    if ex["contractType"] == "PERPETUAL" and ex["quoteAsset"] == "USDT":
        ticker_list.append(ex["pair"])

########################################################################################################################


########################################################################################################################
########################################################################################################################
# Getting price, vol, oi information into respective Pandas DataFrames, utilizing the filtered PERPETUAL USDT tickers

#ticker_samples = [ticker_list[0], ticker_list[1], ticker_list[2], ticker_list[3], ticker_list[4]]
ticker_samples = ticker_list[0:15]
DF_spot = []
DF_futures = []
DF_oi = []
for ticker in ticker_samples:
    req_klines_spot = requests.get("https://api.binance.com/api/v3/klines",
                                   params=dict(symbol=ticker, interval="15m", limit="500"))
    req_klines_spot_result = req_klines_spot.json()
    dataframe_spot = pd.DataFrame(req_klines_spot_result,
                                  columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                           "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                           "Taker Buy Quote Asset Volume", "Ignore"])
    DF_spot.append(dataframe_spot)

    req_klines_futures = requests.get("https://fapi.binance.com/fapi/v1/klines",
                                      params=dict(symbol=ticker, interval="15m", limit="500"))
    req_klines_futures_result = req_klines_futures.json()
    dataframe_futures = pd.DataFrame(req_klines_futures_result,
                                     columns=["Open Time", "Open", "High", "Low", "Close", "Volume", "Close Time",
                                              "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume",
                                              "Taker Buy Quote Asset Volume", "Ignore"])
    DF_futures.append(dataframe_futures)

    req_oi_futures = requests.get("https://fapi.binance.com/futures/data/openInterestHist",
                                  params=dict(symbol=ticker, period="15m", limit="500"))
    req_oi_futures_result = req_oi_futures.json()
    dataframe_oi = pd.DataFrame(req_oi_futures_result,
                                columns=["symbol", "sumOpenInterest", "sumOpenInterestValue", "timestamp"])
    DF_oi.append(dataframe_oi)

########################################################################################################################


########################################################################################################################
########################################################################################################################
# idk what to do next.

oi_arrays = []
oi_array = []
for df in DF_oi:
    oi_array.append(df["sumOpenInterest"].values)
    oi_arrays.append(oi_array)
    oi_array = []

printer = oi_arrays[0][0]
print(printer[0])

printer2 = oi_arrays[1][0]
print(printer2[0])

i = 0
oi_data = []
while i < len(oi_arrays):
    oi_data.append(oi_arrays[i][0])
    print("oi arrays check")
    i += 1

ticker_iterator = 0
for data in oi_data:
    i = 0
    print("NEW OI TICKER IN PROGRESS")
    while i < 490:
        if float(data[i]) > float(data[i+10])*(110/100):
            print(ticker_list[ticker_iterator], "+10% oi increase over t-10th tick, ", i, " time ticks ago")
        elif float(data[i]) > float(data[i+10])*(105/100):
            print(ticker_list[ticker_iterator], "+5% oi increase over t-10th tick, ", i, " time ticks ago")

        i += 1
    print("A LOOP IS OVER")
    ticker_iterator += 1




########################################################################################################################


########################################################################################################################
########################################################################################################################
# Processing the exported Pandas DataFrames
# this currently does not work as intended, so it is commented in
"""
oi_arrays = []
oi_array = []
for df in DF_oi:
    oi_array.append(df["sumOpenInterest"].values)
    oi_arrays.append(oi_array)
    oi_array = []
# print(oi_arrays[0])


# for df in DF_futures:
#    print(df["Close"].values)

# for df in DF_oi:
#    print(df["sumOpenInterest"].values)
"""
########################################################################################################################

"""
# This part gets raw information and prints symbols of json
exchange_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
exchange = exchange_info.json()

f = open("model_outputs/exchangeInfo.txt", "w")
for exch in exchange["symbols"]:
    f.write("%s\n" %exch)
f.close()
"""

"""
# This part creates a filtered list of PERP and USDT pairs to utilize in scanning
exchange_info = requests.get("https://fapi.binance.com/fapi/v1/exchangeInfo")
exchange = exchange_info.json()
exchange_symbols = exchange["symbols"]

f = open("model_outputs/usdt_perpetual_tickers.txt", "w")
for ex in exchange_symbols:
    if ex["contractType"] == "PERPETUAL" and ex["quoteAsset"] == "USDT":
        f.write("%s\n" %ex["pair"])
        #print(ex["pair"])
f.close()
"""
