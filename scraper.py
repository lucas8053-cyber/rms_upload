import os
import sys
# 嘗試多種導入路徑
try:
    from serpapi import GoogleSearch
except ImportError:
    try:
        from google_search_results import GoogleSearch
    except ImportError:
        raise ImportError("無法找到 serpapi 套件，請確認 requirements.txt 已正確包含 serpapi")

def get_hotel_prices(hotel_name, check_in="2026-07-01"):
    # 從 Streamlit Secrets 讀取金鑰
    api_key = st.secrets.get("SERPAPI_KEY")
    
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": check_in,
        "api_key": api_key
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    
    # 提取價格數據
    prices = []
    if "hotels_results" in results:
        for hotel in results["hotels_results"]:
            prices.append({
                "hotel_name": hotel.get("name"),
                "ota_price": hotel.get("rate_per_night", {}).get("lowest"),
                "date": check_in
            })
    return prices
