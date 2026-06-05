import streamlit as st
import sqlite3
import pandas as pd
import subprocess
import os
import sys

# 1. 設定頁面 (只能呼叫一次)
st.set_page_config(page_title="🏨 AI 動態房價決策指揮中心", layout="wide")

# 2. 強制設定網頁語言
st.markdown("""
    <html lang="zh-Hant">
    </html>
""", unsafe_allow_html=True)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db')

# 飯店清單獲取函數
def get_monitored_hotels():
    if not os.path.exists(DB_PATH): return []
    conn = sqlite3.connect(DB_PATH)
    hotels = pd.read_sql_query("SELECT hotel_name FROM monitored_hotels", conn)
    conn.close()
    return hotels['hotel_name'].tolist()

# 側邊欄：飯店管理
st.sidebar.header("飯店設定管理")
new_hotel = st.sidebar.text_input("新增監控飯店名稱")
if st.sidebar.button("新增飯店"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO monitored_hotels (hotel_name) VALUES (?)", (new_hotel,))
    conn.commit()
    conn.close()
    st.rerun()

st.sidebar.write("目前監控中:", get_monitored_hotels())

# 同步按鈕
if st.sidebar.button("🔄 立即同步最新市場數據"):
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
    subprocess.run([sys.executable, script_path], check=True)
    st.rerun()

# 主儀表板
st.title("🏨 AI 動態房價決策中心")

if os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM room_performance", conn)
    conn.close()

    if not df.empty:
        # 重新命名欄位為中文顯示
        display_df = df.drop(columns=['id'], errors='ignore').rename(columns={
            "date": "日期", "hotel_name": "飯店名稱", "room_type": "房型",
            "ota_price": "OTA 售價", "google_search_volume": "搜尋熱度",
            "is_main_room_type": "是否主力", "suggested_price": "建議售價",
            "price_delta": "價格偏差值", "strategy_note": "策略建議"
        })
       # 新增：市場價格趨勢圖
        st.subheader("📊 市場價格動態趨勢")
        if not df.empty:
            # 確保下一行有正確的 4 個空白或是 1 個 Tab 縮排
            pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
            st.line_chart(pivot_df)
        else:
            st.write("尚無足夠歷史數據繪製趨勢圖。")
        st.dataframe(display_df, use_container_width=True)
    else:
        st.info("目前無數據，請點擊左側同步按鈕以載入數據。")
else:
    st.warning("資料庫尚未建立，請先執行 main.py。")
