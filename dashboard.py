import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 市場定價策略分析 (Price Strategy Analysis)")

# 1. 側邊欄
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if h and search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("選擇監控飯店", options=filtered)

if st.sidebar.button("獲取即時定價區間"):
    with st.spinner('正在分析各通路價格策略...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        
        if all_data:
            df = pd.DataFrame(all_data)
            # --- 新增：計算價格廣度 ---
            # 依飯店與通路分組，計算最高價與最低價的差額
            price_spread = df.groupby(['飯店', '訂房通路'])['價格 (TWD)'].agg(['max', 'min']).reset_index()
            price_spread['價格廣度'] = price_spread['max'] - price_spread['min']
            
            # 將廣度資訊併回原表以便顯示
            df = df.merge(price_spread[['飯店', '訂房通路', '價格廣度']], on=['飯店', '訂房通路'])
            st.session_state['price_data'] = df
        else:
            st.error("未找到數據，請確認飯店名稱或稍後再試。")

# 2. 資料展示
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    avg_price = df['價格 (TWD)'].mean()
    
    def highlight_price(val):
        color = 'lightgreen' if val < avg_price else 'lightcoral'
        return f'background-color: {color}'

    st.subheader(f"📊 價格分佈 (市場平均: {avg_price:.0f} TWD)")
    
    # 顯示表格
    st.dataframe(
        df.style.map(highlight_price, subset=['價格 (TWD)']),
        use_container_width=True
    )
    
    # 3. 下載與分析功能
    col1, col2 = st.columns([1, 3])
    with col1:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("📥 下載完整分析數據 (CSV)", csv, "analysis.csv", "text/csv")
    
    st.subheader("各通路價格廣度 (差距越小代表定價越單一)")
    st.bar_chart(df.drop_duplicates(['飯店', '訂房通路']).set_index('訂房通路')['價格廣度'])
    
else:
    st.info("請在左側選擇飯店並開始執行報價查詢。")
