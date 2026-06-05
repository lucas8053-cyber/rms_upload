import streamlit as st
import pandas as pd
import numpy as np

# 設定頁面標題
st.set_page_config(page_title="Hotel RMS Dashboard", layout="wide")

st.title("🏨 飯店營收管理系統 (Cloud Edition)")

# 1. 定義獲取數據的函式 (改為即時抓取模擬數據，未來可對接 API)
def get_market_data():
    # 這裡未來可以替換成你的爬蟲邏輯或 API 呼叫
    # 目前先產生範例數據確保網頁能正常顯示
    try:
        data = {
            'date': pd.date_range(start='2026-06-01', periods=10),
            'hotel_name': ['Vivir Hotel'] * 10,
            'ota_price': np.random.randint(3000, 5000, 10)
        }
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"獲取數據失敗: {e}")
        return pd.DataFrame()

# 2. 執行獲取數據
df = get_market_data()

# 3. 儀表板 UI 邏輯
st.subheader("📊 市場價格動態趨勢")

if not df.empty:
    # 建立 Pivot Table
    pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
    
    # 繪製趨勢圖
    st.line_chart(pivot_df)
    
    # 顯示數據表格
    st.write("最新價格數據表:")
    st.dataframe(df)
else:
    st.warning("⚠️ 系統目前無法獲取數據，請檢查數據來源連線狀態。")

# 4. 側邊欄控制
st.sidebar.header("系統設定")
if st.sidebar.button("手動更新數據"):
    st.rerun()

st.sidebar.info("系統已成功部署於雲端，維運狀態：正常。")
