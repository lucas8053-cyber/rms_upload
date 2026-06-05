import os
from google_search_results import GoogleSearch
import streamlit as st

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
