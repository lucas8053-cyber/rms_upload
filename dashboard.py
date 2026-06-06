import streamlit as st  # 這是最關鍵的一行，必須放在最上方
import pandas as pd
from datetime import datetime
from scraper import get_hotel_prices
from hotels_config import MONITORED_HOTELS

# 緊接著進行設定
st.set_page_config(page_title="飯店收益管理戰情室", layout="wide")
st.title("🏨 飯店收益管理戰情室 (CompSet Analysis)")

# 現在再執行 button 檢查
if st.sidebar.button("同步競爭對手報價"):
    # ... (後續程式碼)
