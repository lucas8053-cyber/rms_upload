import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="專業收益管理儀表板", layout="wide")
st.title("🏨 飯店通路與房型價格監控中心")

# 1. 側邊欄：飯店選擇
st.sidebar.header("1. 選擇飯店")
search_query = st.sidebar.text_input("搜尋飯店名稱")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected_hotels = st.sidebar.multiselect("勾選監控目標", options=filtered)

# 2. 數據獲取按鈕
if st.sidebar.button("獲取即時價格"):
    with st.spinner('正在從 Google 搜尋聚合通路數據...'):
        all_data = []
        for h in selected_hotels:
            all_data.extend(get_hotel_prices(h))
        st.session_state['price_data'] = pd.DataFrame(all_data)

# 3. 呈現邏輯 (含房型動態篩選)
if 'price_data' in st.session_state and not st.session_state['price_data'].empty:
    df = st.session_state['price_data']
    
    st.sidebar.divider()
    st.sidebar.header("2. 篩選房型")
    all_rooms = df['room_type'].unique().tolist()
    selected_rooms = st.sidebar.multiselect("勾選顯示房型", options=all_rooms, default=all_rooms)
    
    # 過濾資料
    display_df = df[df['room_type'].isin(selected_rooms)]
    
    st.subheader(f"📊 {len(selected_hotels)} 家飯店通路報價表")
    st.dataframe(
        display_df.rename(columns={
            'hotel_name': '飯店', 
            'ota_source': '通路', 
            'room_type': '房型', 
            'ota_price': '價格 (TWD)'
        }),
        use_container_width=True
    )
else:
    st.info("請在側邊欄選擇飯店，並點擊「獲取即時價格」。")
