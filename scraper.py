import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_info):
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key: return []

    TARGET_OTAS = ["agoda", "hotels.com", "booking.com", "expedia"]
    url = "https://serpapi.com/search"
    
    # 核心修改：使用 data_id 精確定位
    params = {
        "engine": "google_hotels",
        "data_id": hotel_info["data_id"],
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw",
        "gl": "tw"
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        def find_all_prices(obj, price_list):
            if isinstance(obj, dict):
                if "extracted_lowest" in obj:
                    price_list.append(int(obj["extracted_lowest"]))
                for v in obj.values():
                    find_all_prices(v, price_list)
            elif isinstance(obj, list):
                for item in obj:
                    find_all_prices(item, price_list)

        prices = []
        hotel_data = data.get("hotel_results", data.get("hotels_results", [{}])[0])
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source", "").lower()
                if any(target in ota_name for target in TARGET_OTAS):
                    all_raw_prices = []
                    find_all_prices(source, all_raw_prices)
                    all_raw_prices = [p for p in all_raw_prices if p > 500]
                    
                    if all_raw_prices:
                        prices.append({
                            "飯店": hotel_info["name"],
                            "訂房通路": ota_name.upper(),
                            "價格類型": "最低價",
                            "價格 (TWD)": min(all_raw_prices),
                            "日期": today
                        })
                        prices.append({
                            "飯店": hotel_info["name"],
                            "訂房通路": ota_name.upper(),
                            "價格類型": "最高價",
                            "價格 (TWD)": max(all_raw_prices),
                            "日期": today
                        })
        return prices
    except Exception:
        return []
