import requests
import streamlit as st

def get_hotel_prices(hotel_info):
    api_key = st.secrets.get("SERPAPI_KEY")
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "data_id": hotel_info["data_id"],
        "api_key": api_key,
        "hl": "zh-tw",
        "gl": "tw"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # --- 診斷：直接在介面上顯示 API 回傳內容 ---
        st.write(f"正在除錯 {hotel_info['name']}...")
        st.json(data) # 這會直接把 API 回傳的原始結構印在畫面上
        
        return [] # 先不跑解析，先看數據
    except Exception as e:
        st.error(f"連線失敗: {e}")
        return []
