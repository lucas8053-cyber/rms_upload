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
        "hl": "en",
        "gl": "us",
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # 除錯：直接將原始資料印出來看一下結構，方便找出價格欄位
        # st.write(data.get("hotels_results", [data])[0]) 
        
        prices = []
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                
                # 遍歷可能的價格位置 (有些在 rates，有些在 rooms)
                items = source.get("rooms", []) or source.get("rates", [])
                
                if items:
                    for item in items:
                        name = item.get("name", "Standard")
                        # 這是最關鍵的部分：我們印出每一個 item 試試
                        rate_info = item.get("rate_per_night", {})
                        price = rate_info.get("extracted_lowest")
                        
                        # 增加一個備用方案：有時候價格在 source 本身
                        if not price:
                            price = source.get("rate_per_night", {}).get("extracted_lowest")

                        if price:
                            prices.append({
                                "hotel_name": hotel_data.get("name", hotel_name),
                                "ota_source": ota_name,
                                "room_type": map_room_type(name),
                                "ota_price": int(price),
                                "date": today
                            })
                else:
                    #  fallback
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
        st.error(f"解析發生錯誤: {e}")
        return []
