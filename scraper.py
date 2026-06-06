import requests
import streamlit as st
from datetime import datetime, timedelta

def get_hotel_prices(hotel_name):
    # 搜尋日期設定為今天與明天
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    api_key = st.secrets.get("SERPAPI_KEY")
    if not api_key: 
        st.error("未設定 SERPAPI_KEY")
        return []

    # 指定你要監控的四大 OTA 通路 (轉為小寫以便後續比對)
    TARGET_OTAS = ["agoda", "hotels.com", "booking.com", "expedia"]
    
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_hotels",
        "q": hotel_name, # 若後續改成 Place ID，這裡改為 data_id
        "check_in_date": today,
        "check_out_date": tomorrow,
        "api_key": api_key,
        "currency": "TWD",
        "hl": "en",
        "gl": "tw", # 強制設定 gl=tw，讓搜尋結果更貼近台灣本地市場
        "location": "Taiwan"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # 深度搜尋工具：遞迴遍歷整個 JSON 抓出所有 extracted_lowest
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
        # 從 API 回傳的 hotels_results 抓取飯店資料
        hotel_results = data.get("hotels_results", [])
        if not hotel_results:
            return []
            
        hotel_data = hotel_results[0]
        
        # 遍歷 prices 區域
        if "prices" in hotel_data:
            for source in hotel_data["prices"]:
                ota_name = source.get("source", "").lower()
                
                # 篩選邏輯：只處理我們要的四大通路
                if any(target in ota_name for target in TARGET_OTAS):
                    all_raw_prices = []
                    find_all_prices(source, all_raw_prices)
                    
                    # 過濾異常低價 (500元以下通常不是房價)
                    all_raw_prices = [p for p in all_raw_prices if p > 500]
                    
                    if all_raw_prices:
                        prices.append({
                            "飯店": hotel_data.get("name", hotel_name),
                            "訂房通路": ota_name.upper(),
                            "價格類型": "最低價",
                            "價格 (TWD)": min(all_raw_prices),
                            "日期": today
                        })
                        prices.append({
                            "飯店": hotel_data.get("name", hotel_name),
                            "訂房通路": ota_name.upper(),
                            "價格類型": "最高價",
                            "價格 (TWD)": max(all_raw_prices),
                            "日期": today
                        })
        return prices
    except Exception as e:
        # 在開發時方便除錯，你可以把這行改為 print(e)
        return []
