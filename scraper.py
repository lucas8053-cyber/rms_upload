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
        "q": hotel_name,
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw",
        "gl": "tw",
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        prices = []
        
        # 處理搜尋列表頁 (hotels_results)
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                rate = hotel.get("rate_per_night", {}) or hotel.get("total_rate", {})
                price_raw = rate.get("extracted_lowest") or rate.get("lowest")
                if price_raw:
                    price_str = str(price_raw).replace(',', '').replace('$', '').replace('NT', '')
                    prices.append({"hotel_name": hotel.get("name"), "ota_price": int(float(price_str)), "date": today})
        
        # 處理單一飯店詳細頁 (type: hotel)
        elif data.get("type") == "hotel":
            rate = data.get("rate_per_night", {}) or data.get("total_rate", {})
            price_raw = rate.get("extracted_lowest") or rate.get("lowest")
            if price_raw:
                price_str = str(price_raw).replace(',', '').replace('$', '').replace('NT', '')
                prices.append({"hotel_name": data.get("name"), "ota_price": int(float(price_str)), "date": today})
                
        return prices
    except Exception as e:
        return []
