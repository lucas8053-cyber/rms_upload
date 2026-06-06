import requests
import streamlit as st
from datetime import datetime, timedelta
from mapper import map_room_type

def get_hotel_prices(hotel_name):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "en",  # 強制英文介面
        "gl": "us",  # 配合英文介面設定
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        prices = []
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                rooms = source.get("rooms", [])
                for room in rooms:
                    raw_name = room.get("name", "standard")
                    price = room.get("rate_per_night", {}).get("extracted_lowest")
                    if price:
                        prices.append({
                            "hotel_name": hotel_data.get("name"),
                            "ota_source": source.get("source"),
                            "room_type": map_room_type(raw_name), # 映射後的中文名稱
                            "ota_price": int(price),
                            "date": today
                        })
        return prices
    except:
        return []
