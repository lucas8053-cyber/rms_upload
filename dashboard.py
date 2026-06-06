import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="飯店收益管理戰情室", layout="wide")
st.title("🏨 飯店收益管理戰情室")

if st.sidebar.button("同步競爭對手報價"):
    with st.spinner('正在從 Google Hotels 同步數據...'):
        all_data = []
        for h_info in MONITORED_HOTELS:
            data = get_hotel_prices(h_info)
            if data:
                all_data.extend(data)
        
        if all_data:
            df = pd.DataFrame(all_data)
            df['市場基準價'] = df.groupby('飯店')['價格 (TWD)'].transform('mean')
            df['溢價率(%)'] = ((df['價格 (TWD)'] - df['市場基準價']) / df['市場基準價'] * 100).round(1)
            st.session_state['price_data'] = df
        else:
            st.error("未能獲取數據，請檢查 Place ID 是否正確或是該飯店今日無報價。")

if 'price_data' in st.session_state:
    df = st.session_state['price_data']
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 下載報告", csv, "report.csv", "text/csv")
