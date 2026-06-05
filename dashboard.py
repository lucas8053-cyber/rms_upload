import streamlit as st
import pandas as pd
import numpy as np
from scraper import get_hotel_prices

# 1. 頁面設定
st.set_page_config(page_title="真實市場房價監控", layout="wide")
st.title("🏨 即時市場房價決策中心")

# 2. 外部設定檔導入 (確保你在 GitHub 有建立 hotels_config.py)
try:
    from hotels_config import MONITORED_HOTELS
except ImportError:
    MONITORED_HOTELS = ["Vivir Hotel", "台北君悅酒店", "W Taipei"]

# 3. 數據獲取函式 (處理 API 回傳並過濾空值)
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
        
    return pd.DataFrame(all_data)

# 4. 側邊欄：搜尋與選擇
st.sidebar.header("系統篩選設定")
search_query = st.sidebar.text_input("搜尋飯店關鍵字")
filtered_options = [h for h in MONITORED_HOTELS if search_query.lower() in h.lower()]

selected_hotels = st.sidebar.multiselect(
    "勾選想要監控的飯店", 
    options=filtered_options, 
    default=filtered_options[:1] if filtered_options else []
)

# 5. 數據操作按鈕
if st.sidebar.button("取得最新市場價格"):
    with st.spinner('正在從 Google 搜尋引擎抓取最新房價...'):
        df = get_market_data(selected_hotels)
        st.session_state['market_data'] = df

# 6. 呈現邏輯
if 'market_data' in st.session_state:
    df = st.session_state['market_data']
    
    if not df.empty:
        # KPI 顯示
        avg_price = df['ota_price'].mean()
        col1, col2 = st.columns(2)
        col1.metric("查詢平均房價", f"NT$ {avg_price:,.0f}")
        col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
        
        st.subheader("📊 市場價格趨勢")
        pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
        st.line_chart(pivot_df)
        
        st.write("數據明細表:")
        st.dataframe(df.rename(columns={'date': '日期', 'hotel_name': '飯店名稱', 'ota_price': 'OTA 價格'}), width=None)
    else:
        st.warning("⚠️ 未取得任何數據，請檢查 API 金鑰額度或查詢名稱。")
else:
    st.info("ℹ️ 請先勾選飯店，並點擊左側「取得最新市場價格」按鈕。")
