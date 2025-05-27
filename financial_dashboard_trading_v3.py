
# -*- coding: utf-8 -*-
# 已整合：介面美化、自動時間範圍、預設今天、自訂區間切換等功能
import streamlit as st
import streamlit.components.v1 as stc
import datetime
import pandas as pd

# 樣式美化
st.markdown("""
    <style>
    .main {background-color: #f0f2f6;}
    .stButton>button {
        background-color: #1f4e79;
        color: white;
        border-radius: 10px;
        padding: 0.5em 1em;
    }
    .stDownloadButton>button {
        background-color: #1f4e79;
        color: white;
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 頁首介面
html_temp = """
<div style="background-color:#1f4e79;padding:20px;border-radius:15px">
    <h1 style="color:#ffffff;text-align:center;margin-bottom:5px;">📊 金融看板與程式交易平台</h1>
    <p style="color:#d9e3f0;text-align:center;">Financial Dashboard and Program Trading</p>
</div>
"""
stc.html(html_temp)

# 模擬資料（請替換為實際資料）
df_original = pd.DataFrame({
    'time': pd.date_range(start='2023-01-01', end='2025-05-27', freq='D'),
    'open': [100]*879,
    'close': [105]*879,
    'high': [110]*879,
    'low': [95]*879,
    'volume': [1000]*879
})

# 📅 時間區間選擇
st.markdown("### 📅 選擇時間區間")
min_date = df_original['time'].min().date()
max_date = df_original['time'].max().date()
today = datetime.date.today()
default_end = today if min_date <= today <= max_date else max_date

custom_range = st.checkbox("啟用自訂時間區間", value=False)

if custom_range:
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input('選擇開始日期', value=min_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input('選擇結束日期', value=default_end, min_value=start_date, max_value=max_date)
else:
    start_date = min_date
    end_date = default_end

start_date = datetime.datetime.combine(start_date, datetime.datetime.min.time())
end_date = datetime.datetime.combine(end_date, datetime.datetime.min.time())
df = df_original[(df_original['time'] >= start_date) & (df_original['time'] <= end_date)]

# 🔎 資料摘要
with st.expander("📊 資料統計摘要"):
    st.dataframe(df.describe())

# 📥 匯出資料
st.markdown("### 📥 匯出資料")
st.download_button("⬇️ 下載篩選後資料（CSV）", data=df.to_csv(index=False), file_name="filtered_data.csv")
