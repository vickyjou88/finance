# -*- coding: utf-8 -*-
"""
金融資料視覺化看板 V2 - 加入 RSI, Bollinger Band, MACD 策略交易模組

原始作者: 
修改整合: OpenAI ChatGPT
"""

import os
import numpy as np
import pandas as pd
import datetime
import streamlit as st
import streamlit.components.v1 as stc
import matplotlib.pyplot as plt
from order_streamlit import Record
import indicator_forKBar_short
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 其餘初始化與資料載入請參考原始程式碼，略去冗餘部分

# 策略選單擴充
choices_strategies = [
    '<進場>: MA黃金/死亡交叉, <出場>: 移動停損',
    '<進場>: RSI黃金/死亡交叉, <出場>: 移動停損',
    '<進場>: 觸及布林上下軌反轉操作, <出場>: 移動停損',
    '<進場>: MACD DIF/DEA交叉, <出場>: 移動停損'
]
choice_strategy = st.selectbox('選擇交易策略', choices_strategies, index=0)

OrderRecord = Record()

if choice_strategy == choices_strategies[1]:  # RSI 交叉策略
    for n in range(1, len(KBar_df)-1):
        if not np.isnan(KBar_df['RSI_short'][n-1]) and not np.isnan(KBar_df['RSI_short'][n]):
            if OrderRecord.GetOpenInterest() == 0:
                if KBar_df['RSI_short'][n-1] <= KBar_df['RSI_long'][n-1] and KBar_df['RSI_short'][n] > KBar_df['RSI_long'][n]:
                    OrderRecord.Order('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] - MoveStopLoss
                    continue
                if KBar_df['RSI_short'][n-1] >= KBar_df['RSI_long'][n-1] and KBar_df['RSI_short'][n] < KBar_df['RSI_long'][n]:
                    OrderRecord.Order('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] + MoveStopLoss
                    continue
            elif OrderRecord.GetOpenInterest() > 0:
                if KBar_df['close'][n] < StopLossPoint:
                    OrderRecord.Cover('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    continue
                if KBar_df['close'][n] - MoveStopLoss > StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] - MoveStopLoss
            elif OrderRecord.GetOpenInterest() < 0:
                if KBar_df['close'][n] > StopLossPoint:
                    OrderRecord.Cover('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], -Order_Quantity)
                    continue
                if KBar_df['close'][n] + MoveStopLoss < StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] + MoveStopLoss

elif choice_strategy == choices_strategies[2]:  # 布林通道
    for n in range(1, len(KBar_df)-1):
        if not np.isnan(KBar_df['Upper_Band'][n]) and not np.isnan(KBar_df['Lower_Band'][n]):
            if OrderRecord.GetOpenInterest() == 0:
                if KBar_df['close'][n] < KBar_df['Lower_Band'][n]:
                    OrderRecord.Order('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] - MoveStopLoss
                    continue
                if KBar_df['close'][n] > KBar_df['Upper_Band'][n]:
                    OrderRecord.Order('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] + MoveStopLoss
                    continue
            elif OrderRecord.GetOpenInterest() > 0:
                if KBar_df['close'][n] < StopLossPoint:
                    OrderRecord.Cover('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    continue
                if KBar_df['close'][n] - MoveStopLoss > StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] - MoveStopLoss
            elif OrderRecord.GetOpenInterest() < 0:
                if KBar_df['close'][n] > StopLossPoint:
                    OrderRecord.Cover('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], -Order_Quantity)
                    continue
                if KBar_df['close'][n] + MoveStopLoss < StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] + MoveStopLoss

elif choice_strategy == choices_strategies[3]:  # MACD DIF/DEA策略
    for n in range(1, len(KBar_df)-1):
        if not np.isnan(KBar_df['MACD'][n-1]) and not np.isnan(KBar_df['Signal_Line'][n-1]):
            if OrderRecord.GetOpenInterest() == 0:
                if KBar_df['MACD'][n-1] <= KBar_df['Signal_Line'][n-1] and KBar_df['MACD'][n] > KBar_df['Signal_Line'][n]:
                    OrderRecord.Order('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] - MoveStopLoss
                    continue
                if KBar_df['MACD'][n-1] >= KBar_df['Signal_Line'][n-1] and KBar_df['MACD'][n] < KBar_df['Signal_Line'][n]:
                    OrderRecord.Order('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    StopLossPoint = KBar_df['open'][n+1] + MoveStopLoss
                    continue
            elif OrderRecord.GetOpenInterest() > 0:
                if KBar_df['close'][n] < StopLossPoint:
                    OrderRecord.Cover('Sell', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], Order_Quantity)
                    continue
                if KBar_df['close'][n] - MoveStopLoss > StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] - MoveStopLoss
            elif OrderRecord.GetOpenInterest() < 0:
                if KBar_df['close'][n] > StopLossPoint:
                    OrderRecord.Cover('Buy', KBar_df['product'][n+1], KBar_df['time'][n+1], KBar_df['open'][n+1], -Order_Quantity)
                    continue
                if KBar_df['close'][n] + MoveStopLoss < StopLossPoint:
                    StopLossPoint = KBar_df['close'][n] + MoveStopLoss
