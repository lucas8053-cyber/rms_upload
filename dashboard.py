import streamlit as st
import pandas as pd

st.set_page_config(page_title="收益管理戰情室", layout="wide")
st.title("🏨 收益管理戰情室 (手動同步版)")

# 讀取你的數據檔案
uploaded_file = st.file_uploader("上傳每日市場報價 CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 進行收益管理分析計算
    df['市場基準價'] = df.groupby('飯店')['價格 (TWD)'].transform('mean')
    df['溢價率(%)'] = ((df['價格 (TWD)'] - df['市場基準價']) / df['市場基準價'] * 100).round(1)
    
    # 風險顏色標記
    def style_performance(val):
        color = 'lightcoral' if val > 5 else ('lightgreen' if val < -5 else '')
        return f'background-color: {color}'

    st.subheader("📊 市場定價競爭力報表")
    st.dataframe(
        df.style.map(style_performance, subset=['溢價率(%)']),
        use_container_width=True
    )
    
    # 視覺化各飯店定價分佈
    st.bar_chart(df.pivot(index='飯店', columns='訂房通路', values='價格 (TWD)'))
else:
    st.info("請上傳今日的報價 CSV，系統將自動分析競爭對手的溢價率。")
