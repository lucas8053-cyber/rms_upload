import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="全台飯店營收決策中心", layout="wide")

st.title("🏨 全台飯店動態房價監控系統")

# 1. 自動從觀光署開放資料獲取「全台旅宿清單」
@st.cache_data
def get_full_hotel_list():
    # 使用政府開放資料 CSV (穩定且包含全台)
    url = "https://taiwanstay.net.tw/opendata/hotel_list.csv" 
    try:
        df = pd.read_csv(url)
        # 確保搜尋時包含中文與英文名稱 (若欄位名稱不同，需依實際 CSV 調整)
        return df['hotel_name'].dropna().unique().tolist()
    except:
        return ["Vivir Hotel", "合樂商務", "台北君悅酒店", "W Taipei"]

ALL_HOTELS_DB = get_full_hotel_list()

# 2. 側邊欄：進階搜尋 (解決中文與關鍵字搜尋問題)
st.sidebar.header("系統篩選設定")
search_query = st.sidebar.text_input("輸入飯店名稱關鍵字 (支援中英文)")

# 篩選邏輯：強制轉換為小寫進行比對，確保中英文搜尋皆通
filtered_options = [h for h in ALL_HOTELS_DB if search_query.lower() in h.lower()]

selected_hotels = st.sidebar.multiselect(
    "選擇想要監控的飯店", 
    options=filtered_options, 
    default=filtered_options[:5] if filtered_options else []
)

# 3. 數據模擬函式 (當選定飯店後，即時模擬價格)
def get_price_data(hotel_list):
    if not hotel_list: return pd.DataFrame()
    n_days = 10
    data = []
    for hotel in hotel_list:
        for i in range(n_days):
            data.append({
                '日期': pd.Timestamp.now().date() + pd.Timedelta(days=i),
                '飯店名稱': hotel,
                'OTA 價格': np.random.randint(2500, 8000)
            })
    return pd.DataFrame(data)

# 4. 呈現內容
df = get_price_data(selected_hotels)

if not df.empty:
    avg_price = df['OTA 價格'].mean()
    col1, col2 = st.columns(2)
    col1.metric("所選平均房價", f"NT$ {avg_price:,.0f}")
    col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
    
    st.subheader("📊 市場價格動態趨勢")
    pivot_df = df.pivot_table(index='日期', columns='飯店名稱', values='OTA 價格')
    st.line_chart(pivot_df)
    
    st.write("最新數據明細:")
    st.dataframe(df, use_container_width=True)
else:
    st.info("ℹ️ 請輸入關鍵字搜尋飯店並進行勾選。")
