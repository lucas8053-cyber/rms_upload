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
            price_delta REAL, strategy_note TEXT,
            UNIQUE(date, hotel_name, room_type)
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
            historical_avg_price_increase REAL,
            created_at TEXT
        )
    ''')
    # 分析歷史表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hotel_name TEXT,
            room_type TEXT,
            ota_price REAL,
            google_search_volume INTEGER,
            is_main_room_type INTEGER,
            suggested_price REAL,
            price_delta REAL,
            strategy_note TEXT,
            timestamp TEXT
        )
    ''')
    # 加入索引優化查詢
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_performance_date ON room_performance(date)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_room_performance_hotel ON room_performance(hotel_name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_analysis_history_date ON analysis_history(date)')
    
    # 新增每個 OTA 的報價表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ota_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            hotel_name TEXT,
            room_type TEXT,
            ota_name TEXT,
            ota_price REAL
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_ota_offers_hotel ON ota_offers(hotel_name)')

    # 自動升級舊版資料表 schema
    cursor.execute("PRAGMA table_info(city_events)")
    event_columns = [row[1] for row in cursor.fetchall()]
    if 'created_at' not in event_columns:
        cursor.execute('ALTER TABLE city_events ADD COLUMN created_at TEXT')
    cursor.execute("PRAGMA table_info(room_performance)")
    perf_columns = [row[1] for row in cursor.fetchall()]
    if 'price_delta' not in perf_columns:
        cursor.execute('ALTER TABLE room_performance ADD COLUMN price_delta REAL')
    if 'strategy_note' not in perf_columns:
        cursor.execute('ALTER TABLE room_performance ADD COLUMN strategy_note TEXT')
    cursor.execute("PRAGMA table_info(analysis_history)")
    history_columns = [row[1] for row in cursor.fetchall()]
    if 'timestamp' not in history_columns:
        cursor.execute('ALTER TABLE analysis_history ADD COLUMN timestamp TEXT')

    # 不自動補齊預設監控飯店清單，左側顯示的名單僅依資料庫內實際紀錄。
    conn.commit()
    conn.close()
    print("資料庫結構初始化完成")

def save_scraped_data(df):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    df = df.copy()
    df[['ota_price', 'google_search_volume', 'is_main_room_type', 'suggested_price']] = df[['ota_price', 'google_search_volume', 'is_main_room_type', 'suggested_price']].apply(pd.to_numeric, errors='coerce')
    records = [tuple(row) for row in df[['date', 'hotel_name', 'room_type', 'ota_price', 'google_search_volume', 'is_main_room_type', 'suggested_price']].to_numpy()]
    cursor.executemany(
        '''INSERT OR REPLACE INTO room_performance
           (date, hotel_name, room_type, ota_price, google_search_volume, is_main_room_type, suggested_price)
           VALUES (?, ?, ?, ?, ?, ?, ?)''',
        records
    )
    conn.commit()
    conn.close()
    print("爬蟲數據已寫入資料庫")


def save_ota_offers(df):
    """Save per-OTA offer rows into ota_offers table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    df = df.copy()
    df['ota_price'] = pd.to_numeric(df['ota_price'], errors='coerce')
    records = [tuple(row) for row in df[['date', 'hotel_name', 'room_type', 'ota_name', 'ota_price']].to_numpy()]
    cursor.executemany(
        '''INSERT INTO ota_offers (date, hotel_name, room_type, ota_name, ota_price)
           VALUES (?, ?, ?, ?, ?)''',
        records
    )
    conn.commit()
    conn.close()
    print("OTA 報價已寫入 ota_offers 表")