# dashboard.py (修正縮排版本)

import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="飯店收益管理戰情室", layout="wide")
st.title("🏨 飯店收益管理戰情室 (CompSet Analysis)")

# 這是第 12 行
if st.sidebar.button("同步競爭對手報價"):
    # 以下內容必須全部向右縮排 4 個空格！
    with st.spinner('正在分析各通路與對手定價...'):
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
            st.error("未能獲取任何數據。")
