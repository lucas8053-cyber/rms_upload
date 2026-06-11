import pandas as pd
import sqlite3
import random
import os
import datetime
from database_manager import save_scraped_data, save_ota_offers, DB_PATH

ROOM_TYPES = ["Standard", "Deluxe", "Suite"]
OTA_NAMES = ["Booking.com", "Agoda", "Expedia", "Hotels.com"]


def get_monitored_hotels():
    if not os.path.exists(DB_PATH):
        return []
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT hotel_name FROM monitored_hotels", conn)
        return df['hotel_name'].tolist() if not df.empty else []
    finally:
        conn.close()


def generate_hotel_data(hotel_name, date):
    offers = []
    aggregated = []
    for room in ROOM_TYPES:
        base_price = 2500 + len(hotel_name) * 12 + (300 if room == "Deluxe" else 700 if room == "Suite" else 0)
        for idx, ota_name in enumerate(OTA_NAMES):
            price = base_price + random.randint(-120, 120) + idx * 10
            offers.append({
                "date": date,
                "hotel_name": hotel_name,
                "room_type": room,
                "ota_name": ota_name,
                "ota_price": price
            })

        primary_price = offers[-len(OTA_NAMES)]['ota_price'] if offers else base_price
        aggregated.append({
            "date": date,
            "hotel_name": hotel_name,
            "room_type": room,
            "ota_price": primary_price,
            "google_search_volume": random.randint(40, 120),
            "is_main_room_type": 1 if room == "Suite" else 0,
            "suggested_price": round(primary_price * 1.08, 0)
        })

    offers_df = pd.DataFrame(offers)
    perf_df = pd.DataFrame(aggregated)
    return offers_df, perf_df


def run_scraper():
    today = datetime.date.today().isoformat()
    hotels = get_monitored_hotels()
    if not hotels:
        hotels = ["Taichung Grand Hotel", "Colorful Hotel", "Silk Place Taichung"]

    all_offers = []
    all_perf = []
    for hotel in hotels:
        offers_df, perf_df = generate_hotel_data(hotel, today)
        all_offers.append(offers_df)
        all_perf.append(perf_df)

    if all_offers:
        offers_df = pd.concat(all_offers, ignore_index=True)
        save_ota_offers(offers_df)

    if all_perf:
        perf_df = pd.concat(all_perf, ignore_index=True)
        save_scraped_data(perf_df)


if __name__ == '__main__':
    run_scraper()
