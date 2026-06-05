import pandas as pd
import sqlite3
import os
import datetime
from notifier import send_telegram_msg

# 模擬搜尋活動的 API
def search_event_api(city_query):
    return [{"event_name": "台北熱門演唱會", "event_date": "2026-07-15", "city": "台北"}]

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

    # 1. 計算市場平均與價格偏移
    market_avg = df['ota_price'].mean()
    df['price_delta'] = df['ota_price'] - market_avg
    
    # 2. Telegram 異常警示
    if df['price_delta'].abs().max() > 1000:
        send_telegram_msg("⚠️ 警示：市場定位發生重大偏移！")
        
    # 3. 策略建議
    df['strategy_note'] = df.apply(lambda x: "建議調漲官網價" if x['price_delta'] < 0 else "持平", axis=1)
    
    # 4. 寫入時間戳，確保歷史追蹤
    df['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 5. 關鍵改動：改為 Append，保留歷史資料
    # 注意：我們將結果寫入一個專門存放「歷史分析記錄」的表，避免與原始數據混淆
    df.to_sql('analysis_history', conn, if_exists='append', index=False)
    
    conn.close()
    print("🚀 二次分析報告完成，已追加寫入歷史分析表。")

def check_for_events_and_alert():
    events = search_event_api("台北")
    for event in events:
        hist_data = get_historical_impact(event['city'])
        msg = (f"🔔 市場預警：{event['event_name']} 將於 {event['event_date']} 舉行！\n"
               f"📊 歷史漲幅平均為 {hist_data['increase']}%。\n"
               f"💡 建議提升主力房型售價 15%-20%。")
        send_telegram_msg(msg)