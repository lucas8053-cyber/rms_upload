import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="全台飯店營收決策中心", layout="wide")

st.title("🏨 全台飯店動態房價監控系統")

# 1. 定義你所有想監控的飯店清單 (你可以隨時在這裡增加)
ALL_MONITORED_HOTELS = [
    "Vivir Hotel", "Napas Manor", "Grand Hyatt Taipei", 
    "W Taipei", "Formosa Regent", "Silks Place Tainan"
]

# 2. 數據獲取函式 (模擬全台飯店數據)
def get_market_data():
    n_rows = 50
    data = {
        'date': pd.date_range(start='2026-06-01', periods=n_rows),
        # 隨機分配這些飯店到數據中
        'hotel_name': np.random.choice(ALL_MONITORED_HOTELS, n_rows),
        'ota_price': np.random.randint(2500, 8000, n_rows)
    }
    return pd.DataFrame(data)

df = get_market_data()

# 3. 側邊欄篩選器 - 允許全選或多選
st.sidebar.header("系統篩選設定")
# 改為使用我們預定義的清單，確保使用者能看到所有飯店
selected_hotels = st.sidebar.multiselect(
    "勾選想要監控的飯店", 
    options=ALL_MONITORED_HOTELS, 
    default=["Vivir Hotel", "Napas Manor"] # 預設顯示的飯店
)

# 執行篩選
filtered_df = df[df['hotel_name'].isin(selected_hotels)]

# 4. KPI 統計卡片
if not filtered_df.empty:
    avg_price = filtered_df['ota_price'].mean()
    col1, col2 = st.columns(2)
    col1.metric("所選範圍平均房價", f"NT$ {avg_price:,.0f}")
    col2.metric("監控飯店數量", f"{len(selected_hotels)} 家")
    st.markdown("---")

# 5. 儀表板呈現
st.subheader("📊 市場價格動態趨勢")

if not filtered_df.empty:
    pivot_df = filtered_df.pivot_table(index='date', columns='hotel_name', values='ota_price')
    st.line_chart(pivot_df)
    
    df_display = filtered_df.rename(columns={'date': '日期', 'hotel_name': '飯店名稱', 'ota_price': 'OTA 價格'})
    st.write("最新數據明細:")
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("⚠️ 請從左側邊欄選擇至少一家飯店進行監控。")
