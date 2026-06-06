import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="收益管理戰情室", layout="wide")
st.title("🏨 飯店收益管理戰情室 (CompSet Analysis)")

if st.sidebar.button("同步競爭對手報價"):
    with st.spinner('正在分析各通路與對手定價...'):
        all_data = []
        for h in MONITORED_HOTELS:
            data = get_hotel_prices(h)
            if data:
                all_data.extend(data)
            else:
                st.warning(f"未能抓取到 {h} 的有效數據。")
        
        if all_data:
            df = pd.DataFrame(all_data)
            # 計算該飯店市場基準均價
            df['市場基準價'] = df.groupby('飯店')['價格 (TWD)'].transform('mean')
            # 計算溢價率
            df['溢價率(%)'] = ((df['價格 (TWD)'] - df['市場基準價']) / df['市場基準價'] * 100).round(1)
            st.session_state['price_data'] = df
        else:
            st.error("未能獲取任何數據。")

if 'price_data' in st.session_state:
    df = st.session_state['price_data']
    
    def style_performance(val):
        color = 'lightcoral' if val > 5 else ('lightgreen' if val < -5 else '')
        return f'background-color: {color}'

    st.subheader("📊 競爭對手定價戰情表")
    st.dataframe(
        df.style.map(style_performance, subset=['溢價率(%)']),
        use_container_width=True
    )
    
    # 下載
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 匯出市場報告 (CSV)", csv, f"Market_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    
    st.subheader("市場溢價區間分佈")
    st.bar_chart(df.set_index(['飯店', '訂房通路'])['溢價率(%)'])
