import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理系統", layout="wide")
st.title("🏨 即時市場房型價格監控")

# 側邊欄：選擇
search_query = st.sidebar.text_input("搜尋飯店")
filtered = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]
selected = st.sidebar.multiselect("勾選飯店", options=filtered)

if st.sidebar.button("獲取報價 (自動分類)"):
    all_data = []
    for h in selected:
        all_data.extend(get_hotel_prices(h))
    st.session_state['data'] = pd.DataFrame(all_data)

if 'data' in st.session_state and not st.session_state['data'].empty:
    df = st.session_state['data']
    
    # 房型選擇
    all_rooms = ["標準房", "高級房", "豪華房", "套房", "雙床房", "大床房", "其他"]
    selected_rooms = st.sidebar.multiselect("過濾房型", options=all_rooms, default=all_rooms)
    
    display_df = df[df['room_type'].isin(selected_rooms)]
    
    st.dataframe(display_df.rename(columns={
        'hotel_name': '飯店', 'ota_source': '通路', 
        'room_type': '房型', 'ota_price': '價格'
    }), use_container_width=True)
else:
    st.info("請選擇飯店並執行搜尋。")
