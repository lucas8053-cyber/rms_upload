import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 即時市場通路價格監控")

# 1. 側邊欄：搜尋與選擇
st.sidebar.header("1. 選擇飯店")
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("監控目標飯店", options=filtered)

if st.sidebar.button("獲取即時報價"):
    with st.spinner('正在分析各通路定價...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        st.session_state['price_data'] = pd.DataFrame(all_data)

# 2. 呈現邏輯
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    
    # 計算平均價格以便標記異常
    avg_price = df['ota_price'].mean()
    
    # 建立樣式函數：價格低於平均顯示綠色(促銷)，高於則標記
    def highlight_price(val):
        color = 'lightgreen' if val < avg_price else 'lightcoral'
        return f'background-color: {color}'

    st.subheader(f"📊 市場價格分析 (平均價: {avg_price:.0f} TWD)")
    
    # 欄位重新命名與格式化
    display_df = df.rename(columns={
        'hotel_name': '飯店', 
        'ota_source': '訂房通路', 
        'room_type': '房型', 
        'ota_price': '價格 (TWD)'
    })
    
    # 應用熱力圖樣式 (僅對價格欄位)
    st.dataframe(
        display_df.style.applymap(highlight_price, subset=['價格 (TWD)']),
        use_container_width=True
    )
    
    # 3. 額外分析：各通路價格分佈圖
    st.subheader("通路價格分佈")
    st.bar_chart(df.set_index('ota_source')['ota_price'])
    
else:
    st.info("請在側邊欄選擇飯店，並點擊「獲取即時報價」。")
