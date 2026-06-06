import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 即時市場通路價格監控")

# 1. 側邊欄設定
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("監控目標飯店", options=filtered)

if st.sidebar.button("獲取即時報價"):
    with st.spinner('正在分析各通路定價...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        st.session_state['price_data'] = pd.DataFrame(all_data)

# 2. 數據分析與展示
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    avg_price = df['ota_price'].mean()
    
    def highlight_price(val):
        color = 'lightgreen' if val < avg_price else 'lightcoral'
        return f'background-color: {color}'

    st.subheader(f"📊 市場價格分析 (平均價: {avg_price:.0f} TWD)")
    
    display_df = df.rename(columns={
        'hotel_name': '飯店', 'ota_source': '訂房通路', 
        'room_type': '房型', 'ota_price': '價格 (TWD)', 'date': '日期'
    })
    
    # 顯示表格 (使用 .map 替代 applymap 避免版本錯誤)
    st.dataframe(
        display_df.style.map(highlight_price, subset=['價格 (TWD)']),
        use_container_width=True
    )
    
    # 3. CSV 下載按鈕
    csv = display_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 下載報價數據 (CSV)",
        data=csv,
        file_name=f"hotel_report_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
    
    st.subheader("通路價格分佈圖")
    st.bar_chart(df.set_index('ota_source')['ota_price'])
else:
    st.info("請在左側選擇飯店並執行獲取。")
