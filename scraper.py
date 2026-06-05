import requests
import streamlit as st
import pandas as pd

def get_hotel_prices(hotel_name, check_in="2026-07-01"):
    """
    直接呼叫 SerpApi 的 Google Hotels API，無需安裝 serpapi 套件
    """
    # 從 Streamlit Cloud 的 Secrets 讀取 API 金鑰
    api_key = st.secrets.get("SERPAPI_KEY")
    
    if not api_key:
        st.error("系統未找到 SERPAPI_KEY，請確認在 Streamlit Secrets 中設定正確。")
        return []

    # API 請求設定
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": check_in,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw"  # 指定回傳繁體中文資訊
    }
    
    try:
        # 發送請求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 檢查是否請求成功
        results = response.json()
        
        # 解析數據
        prices = []
        if "hotels_results" in results:
            for hotel in results["hotels_results"]:
                # 取得房價 (如果無法取得則設為 None)
                rate = hotel.get("rate_per_night", {})
                price = rate.get("lowest") if isinstance(rate, dict) else None
                
                prices.append({
                    "hotel_name": hotel.get("name"),
                    "ota_price": price,
                    "date": check_in
                })
        return prices
        
    except requests.exceptions.RequestException as e:
        st.error(f"API 連線錯誤: {e}")
        return []
    except Exception as e:
        st.error(f"數據解析錯誤: {e}")
        return []
