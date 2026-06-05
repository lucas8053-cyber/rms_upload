import streamlit as st
import pandas as pd
from scraper import get_hotel_prices

st.set_page_config(page_title="真實市場房價監控", layout="wide")
st.title("🏨 即時市場房價決策中心")

# 1. 導入設定檔
try:
    from hotels_config import MONITORED_HOTELS
except ImportError:
    MONITORED_HOTELS = ["Vivir Hotel", "台北君悅酒店"]

# 2. 側邊欄篩選
st.sidebar.header("系統篩選設定")
selected_hotels = st.sidebar.multiselect("選擇想要即時查詢的飯店", MONITORED_HOTELS, default=MONITORED_HOTELS[:1])

# 3. 獲取真實 API 數據
if st.sidebar.button("取得最新市場價格"):
    with st.spinner('正在從 Google Hotels 抓取數據...'):
        all_data = []
        for hotel in selected_hotels:
            prices = get_hotel_prices(hotel)
            all_data.extend(prices)
        
        if all_data:
            df = pd.DataFrame(all_data)
            st.session_state['market_data'] = df
        else:
            st.error("未能取得數據，請檢查 API 金鑰或查詢參數。")

# 4. 呈現數據
if 'market_data' in st.session_state:
    df = st.session_state['market_data']
    
    col1, col2 = st.columns(2)
    col1.metric("查詢平均房價", f"NT$ {df['ota_price'].mean():,.0f}")
    
    st.subheader("📊 市場價格趨勢")
    st.line_chart(df.pivot_table(index='date', columns='hotel_name', values='ota_price'))
    st.dataframe(df, use_container_width=True)
else:
    st.info("ℹ️ 請點選左側「取得最新市場價格」按鈕開始監控。")
