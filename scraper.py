import requests
import streamlit as st
from datetime import datetime, timedelta
from mapper import map_room_type  # 確保 mapper.py 在同目錄

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
        "hl": "en",  # 強制英文解析以獲取精確房型單字
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
                rooms = source.get("rooms", [])
                
                # 如果有明確的房型列表
                if rooms:
                    for room in rooms:
                        room_name = room.get("name", "Standard")
                        price = room.get("rate_per_night", {}).get("extracted_lowest")
                        if price:
                            prices.append({
                                "hotel_name": hotel_data.get("name", hotel_name),
                                "ota_source": ota_name,
                                "room_type": map_room_type(room_name), # 透過 mapper 分類
                                "ota_price": int(price),
                                "date": today
                            })
                else:
                    # 沒有房型列表時，嘗試抓取基礎價格並歸類為標準房
                    price_raw = source.get("rate_per_night", {}).get("extracted_lowest")
                    if price_raw:
                        prices.append({
                            "hotel_name": hotel_data.get("name", hotel_name),
                            "ota_source": ota_name,
                            "room_type": "標準房", 
                            "ota_price": int(price_raw),
                            "date": today
                        })
        return prices
    except Exception as e:
        # 顯示錯誤以便除錯
        st.error(f"Scraper Error: {e}")
        return []
