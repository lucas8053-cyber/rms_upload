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
        response.raise_for_status()
        data = response.json()
        
        # 深度搜尋函式：遞迴撈取 JSON 結構中所有名為 extracted_lowest 的價格
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
        hotel_data = data.get("hotels_results", [data])[0] if "hotels_results" in data else data
        
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source")
                all_raw_prices = []
                
                # 強制啟動深度搜尋
                find_all_prices(source, all_raw_prices)
                
                # 過濾掉極端離群值 (例如 < 500 元可能非正常房價)
                all_raw_prices = [p for p in all_raw_prices if p > 500]
                
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
