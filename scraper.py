import pandas as pd
import sqlite3
import random
import os
from database_manager import save_scraped_data

def get_monitored_hotels():
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db')
    conn = sqlite3.connect(DB_PATH)
    hotels = pd.read_sql_query("SELECT hotel_name FROM monitored_hotels", conn)
    conn.close()
    return hotels['hotel_name'].tolist()

def run_scraper():
    competitors = get_monitored_hotels()
    data = []
    room_types = ["Standard", "Deluxe", "Suite"]
    
    for hotel in competitors:
        for room in room_types:
            price = 2500 + (len(hotel) * 20) + (room_types.index(room) * 1000)
            data.append({
               "date": "2026-06-05", "hotel_name": hotel, "room_type": room, 
               "ota_price": price, "google_search_volume": random.randint(50, 100),
               "is_main_room_type": 0, "suggested_price": price
            })
    df = pd.DataFrame(data)
    save_scraped_data(df)