import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 績效數據表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT, hotel_name TEXT, room_type TEXT,
            ota_price REAL, google_search_volume INTEGER,
            is_main_room_type INTEGER, suggested_price REAL,
            price_delta REAL, strategy_note TEXT
        )
    ''')
    # 監控清單表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monitored_hotels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel_name TEXT UNIQUE
        )
    ''')
    # 新增活動數據表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS city_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            city TEXT,
            event_date TEXT,
            impact_score INTEGER,
            historical_avg_price_increase REAL
        )
    ''')
    # 初始化預設清單
    cursor.execute("SELECT count(*) FROM monitored_hotels")
    if cursor.fetchone()[0] == 0:
        default_hotels = ["天月人文休閒汽車旅館", "合樂商務設計旅館", "璽朵精品旅館", "夏都汽車旅館"]
        for h in default_hotels:
            cursor.execute("INSERT OR IGNORE INTO monitored_hotels (hotel_name) VALUES (?)", (h,))
    conn.commit()
    conn.close()
    print("✅ 資料庫結構初始化完成")

def save_scraped_data(df):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql('room_performance', conn, if_exists='append', index=False)
    conn.close()
    print("💾 爬蟲數據已寫入資料庫")