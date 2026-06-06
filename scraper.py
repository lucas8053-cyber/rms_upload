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
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                # 嘗試抓取更多層級的資訊
                rooms = source.get("rooms", [])
                
                # 若找不到 rooms，嘗試抓取是否有更細節的 description
                if not rooms and "room_type" in source:
                     rooms = [{"name": source.get("room_type")}]
                
                if rooms:
                    for room in rooms:
                        price = room.get("rate_per_night", {}).get("extracted_lowest") or source.get("rate_per_night", {}).get("extracted_lowest")
                        if price:
                            prices.append({
                                "hotel_name": hotel_data.get("name", hotel_name),
                                "ota_source": ota_name,
                                "room_type": room.get("name", "未指定房型"),
                                "ota_price": int(price),
                                "date": today
                            })
                else:
                    # 最後防線：若真的都沒有房型資料，回傳基本價格
                    price_raw = source.get("rate_per_night", {}).get("extracted_lowest")
                    if price_raw:
                        prices.append({
                            "hotel_name": hotel_data.get("name", hotel_name),
                            "ota_source": ota_name,
                            "room_type": "未指定房型",
                            "ota_price": int(price_raw),
                            "date": today
                        })
        return prices
    except Exception:
        return []
