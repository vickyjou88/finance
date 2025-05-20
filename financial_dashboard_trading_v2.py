
# financial_dashboard_trading_v2.py
# 更新內容：使用 st.date_input 並限制 end_date >= start_date

import streamlit as st
import pandas as pd
import datetime

# 假設資料的時間範圍
data_start = datetime.date(2022, 1, 1)
data_end = datetime.date(2024, 4, 9)

st.title("金融資料日期選擇示範")

st.subheader("請選擇日期區間")

start_date = st.date_input(
    label="開始日期",
    min_value=data_start,
    max_value=data_end,
    value=data_start,
)

end_date = st.date_input(
    label="結束日期",
    min_value=start_date,  # 自動限制結束日不能早於開始日
    max_value=data_end,
    value=data_end,
)

st.write(f"你選擇的日期區間是：{start_date} 到 {end_date}")
