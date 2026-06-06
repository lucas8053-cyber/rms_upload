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
            # 防護機制：檢查是否為字典，如果不是則忽略或報錯
            if isinstance(h_info, dict) and "data_id" in h_info:
                data = get_hotel_prices(h_info)
                if data:
                    all_data.extend(data)
            else:
                st.warning(f"跳過格式錯誤的項目: {h_info}")
        
        if all_data:
            df = pd.DataFrame(all_data)
            # 計算該飯店市場基準價
            df['市場基準價'] = df.groupby('飯店')['價格 (TWD)'].transform('mean')
            # 計算溢價率
            df['溢價率(%)'] = ((df['價格 (TWD)'] - df['市場基準價']) / df['市場基準價'] * 100).round(1)
            st.session_state['price_data'] = df
        else:
            st.error("未能獲取數據，請確認 Place ID 是否有效，或該飯店今日在 Google Hotels 無對接價格。")

if 'price_data' in st.session_state:
    df = st.session_state['price_data']
    
    # 增加顏色標示：溢價率 > 5% 為紅色， < -5% 為綠色
    st.dataframe(
        df.style.map(lambda x: 'background-color: lightcoral' if x > 5 else ('lightgreen' if x < -5 else ''), subset=['溢價率(%)']),
        use_container_width=True
    )
    
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 下載報告", csv, f"price_report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
