from StockAnalyzer import analysis

#Dependencies: yfinance, pandas, matplotlib 

googleStock = analysis("GOOG", '2018-11-01' , '2020-04-21')

# Variation in %
googleStock.VAR()

# MACD lines (fast and slow) - Default is 12, 26 and 9 days.
googleStock.MACD()

# MACD Histogram
googleStock.MACDhistogram()

# SMA - Simple moving average
googleStock.SMA(15) # Creates SMA of 15 days

# EMA - Exponential moving average
googleStock.EMA(10)  # Creates EMA of 10 days

# EMA - Exponential moving average
googleStock.EMA(50)  # Creates EMA of 50 days

# Plot all the data + indicators
googleStock.plot()
