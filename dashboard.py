import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="多通路房價監控", layout="wide")
st.title("🏨 即時市場通路價格中心")

# 側邊欄篩選
search_query = st.sidebar.text_input("搜尋飯店")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected = st.sidebar.multiselect("選擇飯店", options=filtered)

if st.sidebar.button("取得通路報價"):
    all_prices = []
    for h in selected:
        all_prices.extend(get_hotel_prices(h))
    st.session_state['price_data'] = pd.DataFrame(all_prices)

if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    st.subheader("各大通路報價總覽")
    
    # 顯示格式化表格
    display_df = df.rename(columns={
        'hotel_name': '飯店', 
        'ota_source': '訂房通路', 
        'ota_price': '價格 (TWD)'
    })
    st.dataframe(display_df, use_container_width=True)
else:
    st.info("請選擇飯店並點擊按鈕以獲取報價。")
