import streamlit as st
import pandas as pd
import requests # 假設你用 requests 抓取公開數據

# 1. 建立一個獲取數據的函數
def get_public_market_data():
    # 這裡放入你獲取公開數據的邏輯
    # 例如：呼叫 API 或爬取公開網站
    # data = requests.get("https://api.example.com/data").json()
    
    # 為了測試，我們先回傳一個範例 DataFrame
    data = {
        'date': ['2026-06-05', '2026-06-06'],
        'hotel_name': ['Hotel A', 'Hotel B'],
        'ota_price': [3500, 3800]
    }
    return pd.DataFrame(data)

st.title("🏨 飯店市場公開數據分析")

# 2. 直接在主程式呼叫數據，不需要再連資料庫
df = get_public_market_data()

# 3. 你的儀表板邏輯
if not df.empty:
    pivot_df = df.pivot_table(index='date', columns='hotel_name', values='ota_price')
    st.line_chart(pivot_df)
else:
    st.write("目前無數據。")
