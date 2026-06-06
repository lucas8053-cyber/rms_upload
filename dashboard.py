import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理儀表板", layout="wide")
st.title("🏨 即時市場通路價格中心")

# 1. 側邊欄篩選
st.sidebar.header("1. 搜尋與選取")
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("監控目標飯店", options=filtered)

# 2. 獲取資料
if st.sidebar.button("獲取即時報價"):
    with st.spinner('正在從 Google 聚合通路數據...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        st.session_state['price_data'] = pd.DataFrame(all_data)

# 3. 數據展示與篩選
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    
    st.sidebar.divider()
    st.sidebar.header("2. 房型過濾")
    all_rooms = df['room_type'].unique().tolist()
    selected_rooms = st.sidebar.multiselect("勾選想看的房型", options=all_rooms, default=all_rooms)
    
    # 過濾後的展示
    display_df = df[df['room_type'].isin(selected_rooms)]
    
    st.write(f"目前顯示 {len(selected_hotels)} 家飯店的報價")
    st.dataframe(
        display_df.rename(columns={
            'hotel_name': '飯店', 
            'ota_source': '訂房平台', 
            'room_type': '房型名稱', 
            'ota_price': '價格 (TWD)'
        }),
        use_container_width=True
    )
else:
    st.info("請在左側搜尋飯店並點擊「獲取即時報價」。")
