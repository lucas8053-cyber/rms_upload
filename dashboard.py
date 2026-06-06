import streamlit as st
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

st.set_page_config(page_title="飯店收益管理戰情室", layout="wide")
st.title("🏨 飯店收益管理戰情室 (CompSet Analysis)")

# 1. 快速載入監控清單
if st.sidebar.button("載入全組競爭對手監控"):
    with st.spinner('正在同步市場報價...'):
        all_data = []
        for h in MONITORED_HOTELS:
            all_data.extend(get_hotel_prices(h))
        
        if all_data:
            df = pd.DataFrame(all_data)
            # --- 收益管理核心計算 ---
            # 計算每家飯店的平均市場基準價
            df['市場基準價'] = df.groupby('飯店')['價格 (TWD)'].transform('mean')
            # 計算該通路偏離市場基準的程度 (%)
            df['市場溢價率(%)'] = ((df['價格 (TWD)'] - df['市場基準價']) / df['市場基準價'] * 100).round(1)
            
            st.session_state['price_data'] = df
        else:
            st.warning("數據獲取失敗，請確認網路與 API 連線。")

# 2. 戰情展示
if 'price_data' in st.session_state:
    df = st.session_state['price_data']
    
    # 風險顏色標記函數 (負值綠色=具競爭力，正值紅色=價格偏高)
    def style_performance(val):
        color = 'lightcoral' if val > 5 else ('lightgreen' if val < -5 else '')
        return f'background-color: {color}'

    st.subheader("📊 競爭對手定價戰情表")
    st.dataframe(
        df.style.map(style_performance, subset=['市場溢價率(%)']),
        use_container_width=True
    )
    
    # 3. 戰略洞察
    st.subheader("競爭對手定價廣度比較")
    st.bar_chart(df.drop_duplicates(['飯店', '訂房通路']).set_index('訂房通路')['市場基準價'])

    # 4. 下載分析報告
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 匯出今日市場報告 (CSV)", csv, f"CompSet_Report_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
else:
    st.info("請點擊左側按鈕載入完整的 CompSet 監控數據。")
