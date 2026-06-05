import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="全台飯店營收決策中心", layout="wide")

st.title("🏨 全台飯店動態房價監控系統")

# 1. 獲取飯店清單 (使用觀光署範例，這裡你可以根據需求調整)
@st.cache_data
def get_hotel_list():
    # 這裡放你的全台飯店清單來源
    return ["Vivir Hotel", "Napas Manor", "Grand Hyatt Taipei", "W Taipei", "合樂商務", "台北君悅"]

ALL_MONITORED_HOTELS = get_hotel_list()

# 2. 數據獲取函式 (加入防呆)
def get_market_data(hotel_list):
    # 如果列表為空，直接回傳空的 DataFrame
    if not hotel_list:
        return pd.DataFrame()
    
    n_rows = 50
    data = {
        'date': pd.date_range(start='2026-06-01', periods=n_rows),
        'hotel_name': np.random.choice(hotel_list, n_rows),
        'ota_price': np.random.randint(2500, 8000, n_rows)
    }
    return pd.DataFrame(data)

# 3. 側邊欄篩選器
st.sidebar.header("系統篩選設定")
search_query = st.sidebar.text_input("搜尋飯店名稱 (關鍵字)")

# 篩選邏輯：如果沒搜尋，顯示全部；如果有搜尋，顯示符合的
filtered_options = [h for h in ALL_MONITORED_HOTELS if search_query.lower() in h.lower()]

selected_hotels = st.sidebar.multiselect(
    "勾選想要監控的飯店", 
    options=filtered_options, 
    default=filtered_options[:1] if filtered_options else []
)

# 4. 取得數據 (已包含防呆)
df = get_market_data(selected_hotels)

# 5. 儀表板顯示
if not df.empty:
    avg_price = df['ota_price'].mean()
    col1, col2 = st.columns(2)
    col1.metric("所選平均房價", f"NT$ {avg_price:,.0f}")
    col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
    
    st.subheader("📊 市場價格動態趨勢")
    pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
    st.line_chart(pivot_df)
    
    st.write("最新數據明細:")
    st.dataframe(df.rename(columns={'date': '日期', 'hotel_name': '飯店名稱', 'ota_price': 'OTA 價格'}), use_container_width=True)
else:
    st.warning("⚠️ 目前搜尋結果無資料，請檢查關鍵字或重新選擇飯店。")
