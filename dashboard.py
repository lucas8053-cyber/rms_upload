import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 市場定價區間監控 (深度解析版)")

# 側邊欄
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if h and search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("選擇監控飯店", options=filtered)

if st.sidebar.button("獲取即時定價區間"):
    with st.spinner('正在進行深度解析 (這可能需要幾秒鐘)...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        
        if all_data:
            df = pd.DataFrame(all_data)
            # 計算廣度
            price_spread = df.groupby(['飯店', '訂房通路'])['價格 (TWD)'].agg(['max', 'min']).reset_index()
            price_spread['價格廣度'] = price_spread['max'] - price_spread['min']
            df = df.merge(price_spread[['飯店', '訂房通路', '價格廣度']], on=['飯店', '訂房通路'])
            st.session_state['price_data'] = df
        else:
            st.warning("未抓取到價格，請檢查 API 權限或搜尋條件。")

# 資料展示
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    
    st.subheader("分析報表")
    # 將價格依平均值標記
    avg_price = df['價格 (TWD)'].mean()
    def highlight_price(val):
        return f'background-color: {"lightgreen" if val < avg_price else "lightcoral"}'

    st.dataframe(df.style.map(highlight_price, subset=['價格 (TWD)']), use_container_width=True)
    
    # 下載 CSV
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 下載分析報告", csv, f"report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    # 視覺化
    st.bar_chart(df.drop_duplicates(['飯店', '訂房通路']).set_index('訂房通路')['價格廣度'])
