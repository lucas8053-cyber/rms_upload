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
        response.raise_for_status()
        data = response.json()
        
        prices = []
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                # 策略：優先找 rooms，沒有則找 rates 內的 inclusions，最後才抓總價
                rooms = source.get("rooms", [])
                
                if rooms:
                    for room in rooms:
                        room_name = room.get("name", "標準房型")
                        price = room.get("rate_per_night", {}).get("extracted_lowest")
                        if price:
                            prices.append({"hotel_name": hotel_data.get("name"), "ota_source": ota_name, "room_type": room_name, "ota_price": int(price), "date": today})
                else:
                    # 嘗試抓取 rate 資訊
                    rate_info = source.get("rate_per_night", {})
                    price = rate_info.get("extracted_lowest")
                    if price:
                        prices.append({"hotel_name": hotel_data.get("name"), "ota_source": ota_name, "room_type": "未細分房型", "ota_price": int(price), "date": today})
        return prices
    except Exception:
        return []
