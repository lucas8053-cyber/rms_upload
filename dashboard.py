# dashboard.py 中的獲取迴圈部分
if st.sidebar.button("同步競爭對手報價"):
    with st.spinner('正在鎖定 Place ID 同步市場...'):
        all_data = []
        for h_info in MONITORED_HOTELS: # 這裡傳入字典
            data = get_hotel_prices(h_info)
            if data:
                all_data.extend(data)
        
        # ... (後續計算邏輯保持不變) ...
