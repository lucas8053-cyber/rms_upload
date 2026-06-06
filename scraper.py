import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_info):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    url = "https://serpapi.com/search"
    
    params = {
        "engine": "google_hotels",
        "data_id": hotel_info["data_id"],
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw", # 強制中文
        "gl": "tw"     # 強制台灣視角
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # --- 診斷機制 ---
        # 檢查是否有任何價格欄位
        if "hotel_results" not in data and "hotels_results" not in data:
            st.error(f"【{hotel_info['name']}】API 搜尋結果為空。請確認該飯店在 Google Maps 上是否有開啟「預訂」功能。")
            return []
            
        hotel_data = data.get("hotel_results", data.get("hotels_results", [{}])[0])
        
        if "prices" not in hotel_data:
            st.warning(f"【{hotel_info['name']}】找不到 prices 欄位，該飯店可能未連結任何 OTA。")
            return []
            
        # 正常處理邏輯 (略，與前版相同)
        # ... (後續 find_all_prices 解析邏輯)
        return prices # 請保留你原本的解析部分
    except Exception as e:
        st.error(f"系統錯誤: {str(e)}")
        return []
