import streamlit as st
import pandas as pd
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="真實市場房價監控", layout="wide")
st.title("🏨 即時市場房價決策中心")

def get_market_data(selected_hotels):
    if not selected_hotels:
        return pd.DataFrame(columns=['date', 'hotel_name', 'ota_price'])
        
    all_data = []
    for hotel in selected_hotels:
        prices = get_hotel_prices(hotel)
        if prices:
            all_data.extend(prices)
            
    if not all_data:
        return pd.DataFrame(columns=['date', 'hotel_name', 'ota_price'])
    
    df = pd.DataFrame(all_data)
    df['date'] = pd.to_datetime(df['date'])
    return df

st.sidebar.header("系統篩選設定")
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered_options = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]

selected_hotels = st.sidebar.multiselect("勾選想要監控的飯店", options=filtered_options)

if st.sidebar.button("取得最新市場價格"):
    with st.spinner('正在從 Google 搜尋引擎抓取最新房價...'):
        df = get_market_data(selected_hotels)
        st.session_state['market_data'] = df

if 'market_data' in st.session_state:
    df = st.session_state['market_data']
    if not df.empty:
        avg_price = df['ota_price'].mean()
        col1, col2 = st.columns(2)
        col1.metric("查詢平均房價", f"NT$ {avg_price:,.0f}")
        col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
        
        st.subheader("📊 市場價格趨勢")
        pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
        st.line_chart(pivot_df)
        
        st.write("數據明細表:")
        st.dataframe(df.rename(columns={'date': '日期', 'hotel_name': '飯店名稱', 'ota_price': 'OTA 價格'}), use_container_width=True)
    else:
        st.warning("⚠️ 未取得任何數據，請檢查 API 金鑰或飯店名稱。")
