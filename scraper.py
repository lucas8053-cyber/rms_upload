import requests
import streamlit as st

def get_hotel_prices(hotel_name, check_in="2026-07-01"):
    # 從 Streamlit Secrets 讀取 API Key
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        return []

    # 直接呼叫 API 端點
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": check_in,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw",
        "gl": "tw",          # 強制設定搜尋區域為台灣
        "location": "Taiwan" # 顯式宣告地點為台灣
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        prices = []
        # 從 Google Hotels 回傳結構中提取資料
        if "hotels_results" in data:
            for hotel in data["hotels_results"]:
                rate = hotel.get("rate_per_night", {})
                price = rate.get("lowest")
                if price:
                    # 將價格字串轉換為數字
                    clean_price = int(str(price).replace(',', '').replace('$', ''))
                    prices.append({
                        "hotel_name": hotel.get("name"),
                        "ota_price": clean_price,
                        "date": check_in
                    })
        return prices
    except Exception as e:
        # 將錯誤顯示在頁面上供您參考
        st.error(f"API 請求錯誤: {str(e)}")
        return []
