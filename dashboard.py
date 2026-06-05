import streamlit as st
import pandas as pd
import numpy as np

# 設定頁面，使用寬版配置
st.set_page_config(page_title="飯店營收決策中心", layout="wide")

st.title("🏨 AI 動態房價決策中心")

# 1. 模擬數據獲取 (這裡對接你真實的公開數據來源)
def get_market_data():
    # 這裡將來會換成你的真實爬蟲數據
    data = {
        'date': pd.date_range(start='2026-06-01', periods=10),
        'hotel_name': ['Vivir Hotel', 'Napas Manor', 'Vivir Hotel', 'Napas Manor'] * 3,
        'ota_price': np.random.randint(3000, 5000, 12)
    }
    # 補足數據長度以匹配 DataFrame
    df = pd.DataFrame(data).iloc[:12]
    return df

df = get_market_data()

# 2. 加入飯店篩選器 (解決無法選擇飯店的問題)
st.sidebar.header("系統設定")
all_hotels = df['hotel_name'].unique().tolist()
selected_hotels = st.sidebar.multiselect("選擇監控飯店", all_hotels, default=all_hotels)

# 篩選數據
filtered_df = df[df['hotel_name'].isin(selected_hotels)]

# 3. 處理表頭中文化 (解決表頭英文問題)
df_display = filtered_df.rename(columns={
    'date': '日期',
    'hotel_name': '飯店名稱',
    'ota_price': 'OTA 價格'
})

# 4. 儀表板呈現
st.subheader("📊 市場價格動態趨勢")

if not df_display.empty:
    # 繪圖時使用中文化後的 DataFrame
    pivot_df = df_display.pivot_table(index='日期', columns='飯店名稱', values='OTA 價格')
    st.line_chart(pivot_df)
    
    st.write("最新價格數據表:")
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("⚠️ 請從側邊欄選擇至少一家飯店。")
