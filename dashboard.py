import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="飯店營收決策中心", layout="wide")
st.title("🏨 全台飯店動態房價監控系統")

# 1. 內建一份真實的飯店清單，確保程式可以直接運行
@st.cache_data
def get_hotel_list():
    # 這裡的清單你可以隨意增加
    return [
        "合樂商務旅館", "台北君悅酒店", "W Taipei", "Vivir Hotel", 
        "Napas Manor", "晶華酒店", "福容大飯店", "圓山大飯店", 
        "日月潭涵碧樓", "高雄漢來大飯店"
    ]

ALL_HOTELS_DB = get_hotel_list()

# 2. 側邊欄搜尋與篩選
st.sidebar.header("系統篩選設定")
search_query = st.sidebar.text_input("輸入關鍵字搜尋 (例如: 台北)")

# 篩選邏輯
filtered_options = [h for h in ALL_HOTELS_DB if search_query in h]

selected_hotels = st.sidebar.multiselect(
    "勾選想要監控的飯店", 
    options=filtered_options, 
    default=filtered_options[:1] if filtered_options else []
)

# 3. 數據生成與呈現
if selected_hotels:
    # 模擬數據
    data = []
    for hotel in selected_hotels:
        for i in range(7):
            data.append({'日期': pd.Timestamp.now().date() + pd.Timedelta(days=i), 
                         '飯店名稱': hotel, 
                         'OTA 價格': np.random.randint(2500, 8000)})
    df = pd.DataFrame(data)
    
    st.line_chart(df.pivot_table(index='日期', columns='飯店名稱', values='OTA 價格'))
    st.dataframe(df, use_container_width=True)
else:
    st.info("ℹ️ 請在左側搜尋飯店名稱，並勾選後即可查看數據。")
