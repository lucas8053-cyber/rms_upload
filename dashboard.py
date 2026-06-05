import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="全台飯店營收決策中心", layout="wide")

st.title("🏨 全台飯店動態房價監控系統")

# 1. 自動從觀光署開放資料讀取飯店名單
@st.cache_data # 使用快取，避免每次整理網頁都重新下載
def get_hotel_list():
    # 這是觀光署開放資料的 CSV 網址 (範例)
    url = "https://taiwanstay.net.tw/opendata/hotel_list.csv" 
    try:
        df = pd.read_csv(url)
        # 假設 CSV 欄位名稱為 "hotel_name"，依實際狀況調整
        return df['hotel_name'].unique().tolist()
    except:
        # 若無法連線，回傳備用清單
        return ["Vivir Hotel", "Napas Manor", "Grand Hyatt Taipei"]

ALL_MONITORED_HOTELS = get_hotel_list()

# 2. 模擬房價數據 (未來可對接 API)
def get_market_data(hotel_list):
    n_rows = 100
    data = {
        'date': pd.date_range(start='2026-06-01', periods=n_rows),
        'hotel_name': np.random.choice(hotel_list, n_rows),
        'ota_price': np.random.randint(2500, 8000, n_rows)
    }
    return pd.DataFrame(data)

# 3. 側邊欄：搜尋與選擇
st.sidebar.header("系統篩選設定")
# 使用搜尋框讓你能快速找到飯店
search_query = st.sidebar.text_input("搜尋飯店名稱 (關鍵字)")
filtered_options = [h for h in ALL_MONITORED_HOTELS if search_query.lower() in h.lower()]

selected_hotels = st.sidebar.multiselect(
    "勾選想要監控的飯店", 
    options=filtered_options, 
    default=filtered_options[:5] if filtered_options else []
)

df = get_market_data(selected_hotels)
filtered_df = df[df['hotel_name'].isin(selected_hotels)]

# 4. 呈現內容 (KPI 與圖表同前)
if not filtered_df.empty:
    avg_price = filtered_df['ota_price'].mean()
    col1, col2 = st.columns(2)
    col1.metric("所選平均房價", f"NT$ {avg_price:,.0f}")
    col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
    
    st.line_chart(filtered_df.pivot_table(index='date', columns='hotel_name', values='ota_price'))
else:
    st.info("請搜尋並選擇飯店以開始監控。")
