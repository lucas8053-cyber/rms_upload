import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_name):
    # 設定日期
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        return []

    url = "https://serpapi.com/search"
    # 確保這裡的每一個參數都縮排 4 個空格
    params = {
        "engine": "google_hotels",
        "q": hotel_name + " 台灣",
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
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                rate = hotel.get("rate_per_night", {})
                price = rate.get("lowest")
                if price:
                    clean_price = int(str(price).replace(',', '').replace('$', ''))
                    prices.append({
                        "hotel_name": hotel.get("name"),
                        "ota_price": clean_price,
                        "date": today
                    })
        return prices
    except Exception as e:
        return []
