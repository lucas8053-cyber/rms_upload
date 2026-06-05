import requests
import streamlit as st

def get_hotel_prices(hotel_name, check_in="2026-07-01"):
    """
    使用 requests 呼叫 SerpApi，確保參數傳遞正確
    """
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key:
        return []

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_hotels",
        "q": hotel_name,
        "check_in_date": check_in,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "zh-tw",
        "gl": "tw"
    }
    
    try:
        response = requests.get(url, params=params)
        # 這裡會拋出詳細的錯誤訊息，方便我們偵錯
        response.raise_for_status() 
        results = response.json()
        
        prices = []
        # Google Hotels API 的回傳格式有時是 search_parameters 下，有時是 hotels_results
        if "hotels_results" in results:
            for hotel in results["hotels_results"]:
                rate = hotel.get("rate_per_night", {})
                price = rate.get("lowest") if isinstance(rate, dict) else None
                if price:
                    prices.append({
                        "hotel_name": hotel.get("name"),
                        "ota_price": int(price.replace(',', '')), # 將價格轉為數字
                        "date": check_in
                    })
        return prices
        
    except Exception as e:
        # 在 UI 顯示錯誤，但程式不會崩潰
        st.error(f"API 抓取失敗 ({hotel_name}): {e}")
        return []
