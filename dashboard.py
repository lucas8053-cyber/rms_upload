import streamlit as st
import pandas as pd
import numpy as np

# 設定頁面，使用寬版配置
st.set_page_config(page_title="飯店營收決策中心", layout="wide")

st.title("🏨 AI 動態房價決策中心")

# 1. 數據獲取函式
def get_market_data():
    n_rows = 20
    data = {
        'date': pd.date_range(start='2026-06-01', periods=n_rows),
        'hotel_name': ['Vivir Hotel'] * 10 + ['Napas Manor'] * 10,
        'ota_price': np.random.randint(3000, 6000, n_rows)
    }
    return pd.DataFrame(data)

df = get_market_data()

# 2. 飯店篩選器 (側邊欄)
st.sidebar.header("系統篩選設定")
all_hotels = df['hotel_name'].unique().tolist()
selected_hotels = st.sidebar.multiselect("勾選想要監控的飯店", all_hotels, default=all_hotels)

# 執行篩選
filtered_df = df[df['hotel_name'].isin(selected_hotels)]

# 3. KPI 統計卡片 (顯示在圖表上方)
if not filtered_df.empty:
    avg_price = filtered_df['ota_price'].mean()
    min_price = filtered_df['ota_price'].min()
    
    col1, col2 = st.columns(2)
    col1.metric("所選飯店平均房價", f"NT$ {avg_price:,.0f}")
    col2.metric("監控期間最低房價", f"NT$ {min_price:,.0f}")
    st.markdown("---")

# 4. 儀表板呈現
st.subheader("📊 市場價格動態趨勢")

if not filtered_df.empty:
    # 轉置數據以供繪圖
    pivot_df = filtered_df.pivot_table(index='date', columns='hotel_name', values='ota_price')
    st.line_chart(pivot_df)
    
    # 數據表呈現 (中文化)
    df_display = filtered_df.rename(columns={'date': '日期', 'hotel_name': '飯店名稱', 'ota_price': 'OTA 價格'})
    st.write("最新價格數據明細:")
    st.dataframe(df_display, use_container_width=True)
else:
    st.warning("⚠️ 請從左側邊欄至少選擇一家飯店進行監控。")
