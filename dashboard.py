import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 市場定價區間監控 (Min/Max Pricing)")

# 1. 側邊欄：搜尋與選擇
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("監控目標飯店", options=filtered)

if st.sidebar.button("獲取定價區間"):
    with st.spinner('正在分析各通路價格廣度...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        st.session_state['price_data'] = pd.DataFrame(all_data)

# 2. 數據展示
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    avg_price = df['價格 (TWD)'].mean()
    
    def highlight_price(val):
        color = 'lightgreen' if val < avg_price else 'lightcoral'
        return f'background-color: {color}'

    st.subheader(f"📊 市場定價區間 (平均價: {avg_price:.0f} TWD)")
    
    # 呈現極值表格
    st.dataframe(
        df.style.map(highlight_price, subset=['價格 (TWD)']),
        use_container_width=True
    )
    
    # 3. CSV 下載按鈕
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載價格區間報告 (CSV)",
        data=csv,
        file_name=f"price_range_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
    
    # 4. 可視化比較
    st.subheader("各通路價格區間分佈")
    st.bar_chart(df.set_index(['訂房通路', '價格類型'])['價格 (TWD)'])
else:
    st.info("請在左側選擇飯店並執行獲取。")
