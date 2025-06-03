# indicator_forKBar_short.py

# 載入必要套件
import requests, datetime, os, time
import numpy as np
import matplotlib.dates as mdates

# 算K棒
class KBar():
    # 設定初始化變數
    def __init__(self, date, cycle=1):
        # K棒的頻率(分鐘)
        self.TAKBar = {
            'time': np.array([]),
            'open': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
            'close': np.array([]),
            'volume': np.array([])
        }
        self.current = datetime.datetime.strptime(date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.cycle = datetime.timedelta(minutes=cycle)

    # 更新最新報價
    def AddPrice(self, time, open_price, close_price, low_price, high_price, volume):
        # 沒有任何K棒資料，初始化第一根K棒
        if len(self.TAKBar['close']) == 0:
            self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
            self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
            self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
            self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
            self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
            self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 1  # 新增了第一根K棒

        # 同一根K棒
        if time <= self.current:
            self.TAKBar['close'][-1] = close_price
            self.TAKBar['volume'][-1] += volume
            self.TAKBar['high'][-1] = max(self.TAKBar['high'][-1], high_price)
            self.TAKBar['low'][-1] = min(self.TAKBar['low'][-1], low_price)
            return 0

        # 不同根K棒，更新新的K棒
        while time > self.current:
            self.current += self.cycle
        self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
        self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
        self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
        self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
        self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
        self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
        return 1

    # 取各種欄位資料
    def GetTime(self):
        return self.TAKBar['time']

    def GetOpen(self):
        return self.TAKBar['open']

    def GetHigh(self):
        return self.TAKBar['high']

    def GetLow(self):
        return self.TAKBar['low']

    def GetClose(self):
        return self.TAKBar['close']

    def GetVolume(self):
        return self.TAKBar['volume']

    # 取MA值(MA期數)
    # def GetMA(self,n,matype):
    #     return MA(self.TAKBar,n,matype)    
    # # 取SMA值(SMA期數)
    # def GetSMA(self,n):
    #     return SMA(self.TAKBar,n)
    # # 取WMA值(WMA期數)
    # def GetWMA(self,n):
    #     return WMA(self.TAKBar,n)
    # # 取EMA值(EMA期數)
    # def GetEMA(self,n):
    #     return EMA(self.TAKBar,n)    
    # # 取布林通道值(中線期數)
    # def GetBBands(self,n):
    #     return BBANDS(self.TAKBar,n)   ##BBANDS()函數有很多選項,此處只使用期數 n
    # # RSI(RSI期數)
    # def GetRSI(self,n):
    #     return RSI(self.TAKBar,n)
    # # 取KD值(RSV期數,K值期數,D值期數)
    # def GetKD(self,rsv,k,d):
    #     return STOCH(self.TAKBar,fastk_period = rsv,slowk_period = k,slowd_period = d)
    # # 取得威廉指標        
    # def GetWILLR(self,tp=14):  
    #     return WILLR(self.TAKBar, timeperiod=tp)
    # # 取得乖離率
    # def GetBIAS(self,tn=10):
    #     mavalue=MA(self.TAKBar,timeperiod=tn,matype=0)
    #     return (self.TAKBar['close']-mavalue)/mavalue



            
