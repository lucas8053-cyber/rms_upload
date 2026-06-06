import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_name):
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
        "hl": "zh-tw",
        "gl": "tw",
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        prices = []
        
        # 取得飯店資料區塊
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        # 遍歷所有通路價格
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                # 獲取價格，並移除無關字符
                price_raw = source.get("rate_per_night", {}).get("extracted_lowest")
                if ota_name and price_raw:
                    prices.append({
                        "hotel_name": hotel_data.get("name", hotel_name),
                        "ota_source": ota_name,
                        "ota_price": int(price_raw),
                        "date": today
                    })
        return prices
    except Exception:
        return []
