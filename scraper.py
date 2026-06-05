import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_name):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        return []

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,           # 直接使用原始名稱，不要加"台灣"
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw",             # 繁體中文
        "gl": "tw",                # 【關鍵】強制設為台灣地區
        "location": "Taiwan"       # 【關鍵】明確範圍限制在台灣
    }
    
   try:
        response = requests.get(url, params=params)
        data = response.json()
        
        prices = []
        
        # 邏輯 1: 如果是搜尋列表頁 (hotels_results)
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                rate = hotel.get("rate_per_night", {}) or hotel.get("total_rate", {})
                price = rate.get("extracted_lowest") or rate.get("lowest")
                if price:
                    prices.append({"hotel_name": hotel.get("name"), "ota_price": int(price), "date": today})
        
        # 邏輯 2: 如果是單一飯店詳細資訊頁 (直接回傳的屬性)
        elif "type" in data and data["type"] == "hotel":
            rate = data.get("rate_per_night", {}) or data.get("total_rate", {})
            price = rate.get("extracted_lowest") or rate.get("lowest")
            if price:
                prices.append({"hotel_name": data.get("name"), "ota_price": int(price), "date": today})
                
        return prices
    except Exception as e:
        st.error(f"解析錯誤: {e}")
        return []
