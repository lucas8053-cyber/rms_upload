import pandas as pd
import sqlite3
import random
import os
import datetime
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
    
    today = datetime.date.today().isoformat()
    ota_names = ["Booking.com", "Agoda", "Expedia", "Hotels.com"]
    offers = []
    aggregated = []
    for hotel in competitors:
        for room in room_types:
            baseline = 2500 + (len(hotel) * 20)
            room_markup = 800 if room == "Deluxe" else 1400 if room == "Suite" else 0
            base_price = baseline + room_markup
            # produce multiple ota offers with small variations
            for idx, ota in enumerate(ota_names):
                price = base_price + random.randint(-100, 100) + (idx * 10)
                offers.append({
                    "date": today,
                    "hotel_name": hotel,
                    "room_type": room,
                    "ota_name": ota,
                    "ota_price": price
                })
            # aggregated main record (use first OTA as primary)
            primary_price = offers[-len(ota_names)]['ota_price'] if offers else base_price
            aggregated.append({
               "date": today,
               "hotel_name": hotel,
               "room_type": room,
               "ota_price": primary_price,
               "google_search_volume": random.randint(50, 100),
               "is_main_room_type": 1 if room == "Deluxe" else 0,
               "suggested_price": round(primary_price * 1.05, 0)
            })

    offers_df = pd.DataFrame(offers)
    agg_df = pd.DataFrame(aggregated)
    from database_manager import save_ota_offers, save_scraped_data
    if not offers_df.empty:
        save_ota_offers(offers_df)
    if not agg_df.empty:
        save_scraped_data(agg_df)