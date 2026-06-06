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
        "hl": "en",
        "gl": "us",
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        prices = []
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                # 收集該通路下的所有價格
                all_raw_prices = []
                items = source.get("rooms", []) or source.get("rates", [])
                
                # 若有明細則收集所有價格，無明細則取單一價格
                if items:
                    for item in items:
                        p = item.get("rate_per_night", {}).get("extracted_lowest")
                        if p: all_raw_prices.append(int(p))
                else:
                    p = source.get("rate_per_night", {}).get("extracted_lowest")
                    if p: all_raw_prices.append(int(p))
                
                # 加入最高與最低價記錄
                if all_raw_prices:
                    prices.append({
                        "飯店": hotel_data.get("name", hotel_name),
                        "訂房通路": ota_name,
                        "價格類型": "最低價",
                        "價格 (TWD)": min(all_raw_prices),
                        "日期": today
                    })
                    prices.append({
                        "飯店": hotel_data.get("name", hotel_name),
                        "訂房通路": ota_name,
                        "價格類型": "最高價",
                        "價格 (TWD)": max(all_raw_prices),
                        "日期": today
                    })
        return prices
    except Exception as e:
        st.error(f"Scraper Error: {e}")
        return []
