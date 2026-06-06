import requests
import streamlit as st
from datetime import datetime, timedelta
from mapper import map_room_type

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
        "hl": "en",
        "gl": "us",
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
                # 遍歷 rooms 或 rates
                items = source.get("rooms", []) or source.get("rates", [])
                
                if items:
                    for item in items:
                        name = item.get("name", "Standard")
                        price = item.get("rate_per_night", {}).get("extracted_lowest")
                        if price:
                            prices.append({
                                "hotel_name": hotel_data.get("name", hotel_name),
                                "ota_source": ota_name,
                                "room_type": map_room_type(name),
                                "ota_price": int(price),
                                "date": today
                            })
                else:
                    price = source.get("rate_per_night", {}).get("extracted_lowest")
                    if price:
                        prices.append({
                            "hotel_name": hotel_data.get("name", hotel_name),
                            "ota_source": ota_name,
                            "room_type": "Standard",
                            "ota_price": int(price),
                            "date": today
                        })
        return prices
    except Exception as e:
        st.error(f"Scraper Error: {e}")
        return []
