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
        data = response.json()
        
        prices = []
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                # 彈性抓取路徑：有些在 rate_per_night，有些在 total_rate
                rate_info = hotel.get("rate_per_night") or hotel.get("total_rate") or {}
                price = rate_info.get("extracted_lowest") or rate_info.get("lowest")
                
                if price:
                    # 確保是數字
                    clean_price = int(str(price).replace(',', '').replace('$', ''))
                    prices.append({
                        "hotel_name": hotel.get("name", hotel_name),
                        "ota_price": clean_price,
                        "date": today
                    })
        return prices
    except Exception as e:
        return []
