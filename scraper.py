import requests
import streamlit as st
from datetime import datetime, timedelta

from datetime import datetime, timedelta

def get_hotel_prices(hotel_name):
    # 自動獲取「今天」為入住日，「明天」為退房日
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key: return []

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw"
    }
    # ... (後續解析代碼與之前相同)
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # --- 新增這行來檢查 ---
        st.write("API 回傳原始數據:", data) 
        # ---------------------
        
        prices = []
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                rate = hotel.get("rate_per_night", {})
                price = rate.get("lowest")
                if price:
                    clean_price = int(str(price).replace(',', '').replace('$', ''))
                    prices.append({
                        "hotel_name": hotel.get("name"),
                        "ota_price": clean_price,
                        "date": check_in
                    })
        return prices
    except Exception as e:
        st.error(f"API 請求錯誤: {str(e)}")
        return []
