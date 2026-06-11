import pandas as pd
import sqlite3
import os
import datetime

# 模擬搜尋活動的 API
# 只回傳會造成大量客房需求的台中重大活動
def search_event_api(city_query):
    if "台中" in city_query or "Taichung" in city_query:
        return [
            {"event_name": "台中巨蛋演唱會", "event_date": "2026-07-20", "city": "台中"},
            {"event_name": "台中馬拉松路跑", "event_date": "2026-08-03", "city": "台中"},
            {"event_name": "國定連假-中秋連假", "event_date": "2026-09-19", "city": "台中"},
            {"event_name": "國慶日-雙十節", "event_date": "2026-10-10", "city": "台中"}
        ]
    return []

def get_historical_impact(city):
    return {"increase": 25}

def calculate_and_update_strategy():
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db')
    conn = sqlite3.connect(DB_PATH)
    # 讀取最近一次的爬蟲數據 (假設爬蟲將數據存入 temporary_data 表或最後一批)
    # 這裡我們讀取 room_performance 的最新快照
    df = pd.read_sql_query("SELECT * FROM room_performance ORDER BY id DESC LIMIT 12", conn)
    
    if df.empty:
        print("⚠️ 資料庫為空")
        conn.close()
        return

    # 強制轉換數值欄位，避免資料庫型態問題
    for col in ['ota_price', 'google_search_volume', 'is_main_room_type', 'suggested_price']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 1. 計算市場平均與價格偏移
    market_avg = df['ota_price'].mean()
    if pd.isna(market_avg):
        print("⚠️ 無法計算市場平均價，請檢查資料格式。")
        conn.close()
        return
    df['price_delta'] = df['ota_price'] - market_avg
    
    # 2. 異常警示
    if df['price_delta'].abs().max() > 1000:
        print("⚠️ 警示：市場定位發生重大偏移！")
    
    # 3. 策略建議
    df['strategy_note'] = df.apply(lambda x: "建議調漲官網價" if x['price_delta'] < 0 else "持平", axis=1)
    
    # 4. 寫入時間戳，確保歷史追蹤
    df['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 5. 關鍵改動：改為 Append，保留歷史資料
    # 注意：我們將結果寫入一個專門存放「歷史分析記錄」的表，避免與原始數據混淆
    df.to_sql('analysis_history', conn, if_exists='append', index=False)
    # 同步更新 room_performance 的策略與偏差欄位
    cursor = conn.cursor()
    update_records = df[['price_delta', 'strategy_note', 'date', 'hotel_name', 'room_type']].to_records(index=False)
    cursor.executemany(
        '''UPDATE room_performance
           SET price_delta = ?, strategy_note = ?
           WHERE date = ? AND hotel_name = ? AND room_type = ?''',
        update_records
    )
    conn.commit()
    conn.close()
    print("二次分析報告完成，已追加寫入歷史分析表。")

def check_for_events_and_alert():
    events = search_event_api("台中")
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db'))
    cursor = conn.cursor()
    cursor.execute("DELETE FROM city_events WHERE city = '台中' AND event_name LIKE '%週年慶%'")
    conn.commit()
    if not events:
        conn.close()
        return
    for event in events:
        hist_data = get_historical_impact(event['city'])
        print(f"市場預警：{event['event_name']} 將於 {event['event_date']} 舉行！")
        print(f"歷史漲幅平均為 {hist_data['increase']}%。")
        print("建議提升主力房型售價 15%-20%。")
        cursor.execute(
            "SELECT 1 FROM city_events WHERE event_name = ? AND city = ? AND event_date = ? LIMIT 1",
            (event['event_name'], event['city'], event['event_date'])
        )
        if cursor.fetchone() is None:
            cursor.execute(
                '''INSERT INTO city_events (event_name, city, event_date, impact_score, historical_avg_price_increase, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (event['event_name'], event['city'], event['event_date'], 1, hist_data['increase'], datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
    conn.commit()
    conn.close()