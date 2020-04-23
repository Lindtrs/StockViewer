import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class analysis:

   def __init__ (self, stock, date1, date2):
      
      self.stock = stock
      self.data = yf.download(self.stock , date1, date2)

      self.plotsSMA = []
      self.plotsEMA = []
      self.plotsVAR = []
      self.plotsMACD = []
      self.plotsHistMACD = [] 

   def SMA (self, n , plot=True , data=[]):

      if len(data) == 0:

         data = self.data['Close']

      sma = []

      for i in range (0, n-1):

         sma.append(data[0])

      for i in range (n-1 , len(data)):

         soma = 0

         for j in range (0, n):

            soma += data[i-j]

         sma.append(soma / n)

      if plot == True:

         self.data.insert(len(self.data.columns), 'sma' + str(n), sma)
         self.plotsSMA.append('sma' + str(n))

      return sma

   def EMA (self, n , plot=True , data=[]):

      if len(data) == 0:
         
         data = self.data['Close']

      ema = [data[0]]
      k = 2/(n+1)

      for i in range (1, len(data)):

         ema.append(data[i] * k + ema[len(ema)-1] * (1-k))

      if plot == True:
         
         self.data.insert(len(self.data.columns), 'ema' + str(n), ema)
         self.plotsEMA.append('ema' + str(n))
      
      return ema

   def VAR (self, plot=True , data=[]):

      if len(data) == 0:

         data = self.data['Close']

      var = []
      var.append(0)

      for i in range (1, len(data)):

         closeToday = data[i]
         closeYesterday = data[i-1]

         var.append((closeToday/closeYesterday - 1)*100)

      if plot == True:

         self.data.insert(len(self.data.columns), 'var', var)
         self.plotsVAR.append('var')

      return var

   def MACD (self, plot=True):

      ema12 = self.EMA(12, plot=False)
      ema26 = self.EMA(26, plot=False)
   
      fastMACD = []

      for i in range (len(ema12)):
      
         fastMACD.append(int(ema26[i]) - int(ema12[i]))

      slowMACD = []
      slowMACD = self.EMA(9, plot=False, data=fastMACD)

      if plot == True:

         self.data.insert(len(self.data.columns), 'fastMACD', fastMACD)
         self.plotsMACD.append('fastMACD')
         self.data.insert(len(self.data.columns), 'slowMACD', slowMACD)
         self.plotsMACD.append('slowMACD')

      return fastMACD, slowMACD

   def MACDhistogram (self):

      fastMACD , slowMACD = self.MACD(plot=False)

      MACDhist = []

      for i in range (len(fastMACD)):

         MACDhist.append(fastMACD[i] - slowMACD[i])

      self.data.insert(len(self.data.columns), 'MACDhist', MACDhist)   
      self.plotsHistMACD.append('MACDhist')


   def plot (self):

      numberAxes = 0
      plots = []

      if len(self.plotsVAR) != 0:
         numberAxes += 1
         plots.append('var')
      if len(self.plotsMACD) != 0:
         numberAxes += 1
         plots.append('macd')
      if len(self.plotsHistMACD)!= 0:
         numberAxes += 1
         plots.append('MACDhist')

      if numberAxes == 0:

         self.data['Close'].plot(grid=True, label=self.stock)

         for i in self.plotsSMA:

            self.data[i].plot(grid=True, label=i.upper())

         for i in self.plotsEMA:

            self.data[i].plot(grid=True, label=i.upper())

         plt.legend()

      if numberAxes == 1:

         fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(6, 6), gridspec_kw={'height_ratios': [3, 1]})
         
         ax1.plot(self.data.index , self.data['Close'] , '-' , label=self.stock)

         for i in self.plotsSMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i)

         for i in self.plotsEMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i)

         ax1.legend()

         axes = [ax2]

         for i in range (numberAxes):

            if plots[i] == 'macd':
               axes[i].plot(self.data.index, self.data['fastMACD'], label='Fast MACD') 
               axes[i].plot(self.data.index, self.data['slowMACD'], label='Slow MACD')
            elif plots[i] == 'MACDhist':
               axes[i].plot(self.data.index, self.data[plots[i]] , label='MACD Hist.')
               axes[i].fill_between(self.data.index , self.data['MACDhist'])
            else:
               axes[i].plot(self.data.index, self.data[plots[i]], label='Var%')
               
            axes[i].legend()


      if numberAxes == 2:

         fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(6, 6), gridspec_kw={'height_ratios': [3, 1 , 1]})
         
         ax1.plot(self.data.index , self.data['Close'] , '-' , label=self.stock)

         for i in self.plotsSMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i.upper())

         for i in self.plotsEMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i.upper())

         ax1.legend()

         axes = [ax2, ax3]

         for i in range (numberAxes):

            if plots[i] == 'macd':
               axes[i].plot(self.data.index, self.data['fastMACD'], label='Fast MACD') 
               axes[i].plot(self.data.index, self.data['slowMACD'], label='Slow MACD')
            elif plots[i] == 'MACDhist':
               axes[i].plot(self.data.index, self.data[plots[i]] , label='MACD Hist.')
               axes[i].fill_between(self.data.index , self.data['MACDhist'])
            else:
               axes[i].plot(self.data.index, self.data[plots[i]], label='Var%')
               
            axes[i].legend()

      if numberAxes == 3:

         fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(6, 6), gridspec_kw={'height_ratios': [3, 1, 1,1]})
         
         ax1.plot(self.data.index , self.data['Close'] , '-' , label=self.stock)

         for i in self.plotsSMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i.upper())

         for i in self.plotsEMA:

            ax1.plot(self.data.index , self.data[i] , '-' , label=i.upper())

         ax1.legend()

         axes = [ax2, ax3 , ax4]

         for i in range (numberAxes):

            if plots[i] == 'macd':
               axes[i].plot(self.data.index, self.data['fastMACD'], label='Fast MACD') 
               axes[i].plot(self.data.index, self.data['slowMACD'], label='Slow MACD')
            elif plots[i] == 'MACDhist':
               axes[i].plot(self.data.index, self.data[plots[i]] , label='MACD Hist.')
               axes[i].fill_between(self.data.index , self.data['MACDhist'])
            else:
               axes[i].plot(self.data.index, self.data[plots[i]], label='Var%')
               
            axes[i].legend()


      plt.legend()
      plt.show()



