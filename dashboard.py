import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

# 介面設定
st.set_page_config(page_title="客房價格比價系統", layout="wide")
st.title("🏨 客房價格比價系統 (CompSet Analysis)")

# 1. 側邊欄選擇
search_query = st.sidebar.text_input("搜尋飯店")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("監控飯店", options=filtered)

if st.sidebar.button("執行比價"):
    all_data = []
    for h in selected_hotels:
        all_data.extend(get_hotel_prices(h))
    st.session_state['data'] = pd.DataFrame(all_data)

# 2. 數據顯示
if 'data' in st.session_state and not st.session_state['data'].empty:
    df = st.session_state['data']
    
    # 核心房型篩選
    room_options = ["Suite", "Deluxe", "Superior", "Standard"]
    selected_rooms = st.sidebar.multiselect("篩選房型", options=room_options, default=room_options)
    
    display_df = df[df['room_type'].isin(selected_rooms)]
    
    st.subheader("原始數據診斷")
    st.write(df) # 這會把整個 DataFrame 顯示出來，包含原始名稱
    
    st.subheader("分類後的數據表")
    st.dataframe(display_df.rename(columns={
        'hotel_name': '飯店', 
        'ota_source': '訂房通路', 
        'room_type': '房型級距', 
        'ota_price': '價格 (TWD)'
    }), use_container_width=True)
    
    # 統計分析：各級距房價分佈
    st.subheader("各級距房價平均")
    st.bar_chart(display_df.groupby('room_type')['ota_price'].mean())
else:
    st.info("請選擇飯店並執行比價以查看數據。")
