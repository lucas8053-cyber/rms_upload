import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('hotel_rms.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_performance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            room_type TEXT,
            ota_price REAL,
            google_search_volume INTEGER,
            is_main_room_type INTEGER,
            suggested_price REAL
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ 資料庫結構初始化完成")

# 用來接收 scraper 爬到的數據
def save_scraped_data(df):
    conn = sqlite3.connect('hotel_rms.db')
    # 將爬取的數據追加到資料庫
    df.to_sql('room_performance', conn, if_exists='append', index=False)
    conn.close()
    print("💾 爬蟲數據已寫入資料庫")