import numpy
import talib
import json
import pandas as pd
import matplotlib.pyplot as plt

#close = numpy.random.random(100)
#print(close)
#ma = talib.SMA(close)

filename = "BCPTBTC-11-14-2020 23-30-23.txt"
trade_dump = open("../logs/" + filename, "r")
trades = trade_dump.readlines()
t_data = list()
for trade in trades:
    t_data.append(json.loads(trade))

df = pd.DataFrame(t_data)
df["price"] = (pd.to_numeric(df["p"]) * 100000000) - 100

df['RSI'] = talib.RSI(df['price'], 10)
#df['MACD'] = talib.MACD(df['price'])
df['EMA'] = talib.EMA(df['price'], timeperiod=12)
df['SMA'] = talib.SMA(df['price'], timeperiod=12)
df['SMA5'] = talib.SMA(df['price'], timeperiod=5)


fig = plt.figure()
#ax1 = fig.add_subplot(111)
#ax1.plot(df['RSI'], marker='.', color='g', label="RSI")

ax2 = fig.add_subplot(221)
ax2.plot(df['SMA'], marker='.', color='b', label="RSI")


ax4 = fig.add_subplot(221)
ax4.plot(df['price'], marker='*', color='r', label="Price")

#ax1.grid()
#ax2.grid()
#ax3.grid()
#ax4.grid()

#c = df[['RSI', 'price', 'SMA', 'EMA']].plot(subplots=True)

plt.show()
