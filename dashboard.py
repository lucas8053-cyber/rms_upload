import streamlit as st
import pandas as pd
import numpy as np

# 設定頁面，使用寬版配置
st.set_page_config(page_title="飯店營收決策中心", layout="wide")

st.title("🏨 AI 動態房價決策中心")

# 1. 修正數據產生邏輯，確保長度絕對一致
def get_market_data():
    # 設定相同的資料筆數
    n_rows = 10
    data = {
        'date': pd.date_range(start='2026-06-01', periods=n_rows),
        'hotel_name': ['Vivir Hotel'] * 5 + ['Napas Manor'] * 5,
        'ota_price': np.random.randint(3000, 5000, n_rows)
    }
    df = pd.DataFrame(data)
    return df

df = get_market_data()

# 2. 加入飯店篩選器
st.sidebar.header("系統設定")
all_hotels = df['hotel_name'].unique().tolist()
selected_hotels = st.sidebar.multiselect("選擇監控飯店", all_hotels, default=all_hotels)

# 篩選數據
filtered_df = df[df['hotel_name'].isin(selected_hotels)]

# 3. 處理表頭中文化
df_display = filtered_df.rename(columns={
    'date': '日期',
    'hotel_name': '飯店名稱',
    'ota_price': 'OTA 價格'
})

# 4. 儀表板呈現
st.subheader("📊 市場價格動態趨勢")

if not df_display.empty:
    # 這裡使用 pivot_table 轉置數據以繪圖
    pivot_df = df_display.pivot_table(index='日期', columns='飯店名稱', values='OTA 價格')
    st.line_chart(pivot_df)
    
    st.write("最新價格數據表:")
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("⚠️ 請從側邊欄選擇至少一家飯店。")
