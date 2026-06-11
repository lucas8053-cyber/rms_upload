import streamlit as st
import sqlite3
import pandas as pd
import subprocess
import os
import sys
from database_manager import init_db

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotel_rms.db')

st.set_page_config(page_title="🏨 AI 動態房價決策指揮中心", layout="wide")

# 確保資料庫已建立，避免 sidebar 讀取時發生錯誤
try:
    init_db()
except Exception:
    pass

# 飯店清單獲取函數

def get_monitored_hotels():
    if not os.path.exists(DB_PATH):
        return []
    try:
        conn = sqlite3.connect(DB_PATH)
        hotels = pd.read_sql_query("SELECT hotel_name FROM monitored_hotels", conn)
        conn.close()
        return hotels['hotel_name'].tolist()
    except Exception as exc:
        st.sidebar.warning(f"讀取監控飯店失敗：{exc}")
        return []

# 側邊欄：飯店管理
st.sidebar.header("飯店設定管理")
new_hotel = st.sidebar.text_input("新增監控飯店名稱")
if st.sidebar.button("新增飯店"):
    if not new_hotel.strip():
        st.sidebar.warning("請輸入飯店名稱後再新增。")
    elif not os.path.exists(DB_PATH):
        st.sidebar.error("資料庫尚未建立，請先執行 main.py。")
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO monitored_hotels (hotel_name) VALUES (?)", (new_hotel.strip(),))
            conn.commit()
            conn.close()
            st.sidebar.success("已新增監控飯店。")
            st.rerun()
        except Exception as exc:
            st.sidebar.error(f"新增飯店失敗：{exc}")

monitored_hotels = get_monitored_hotels()
st.sidebar.subheader("目前監控中")
if monitored_hotels:
    st.sidebar.markdown("\n".join(f"- {hotel}" for hotel in monitored_hotels))
    selected_to_delete = st.sidebar.selectbox("選取要刪除的監控飯店", monitored_hotels, key="delete_select")
    if st.sidebar.button("刪除選取飯店", key="delete_btn"):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("DELETE FROM monitored_hotels WHERE hotel_name = ?", (selected_to_delete,))
            cur.execute("DELETE FROM room_performance WHERE hotel_name = ?", (selected_to_delete,))
            cur.execute("DELETE FROM ota_offers WHERE hotel_name = ?", (selected_to_delete,))
            cur.execute("DELETE FROM analysis_history WHERE hotel_name = ?", (selected_to_delete,))
            conn.commit()
            conn.close()
            st.sidebar.success(f"已刪除：{selected_to_delete}")
            st.rerun()
        except Exception as exc:
            st.sidebar.error(f"刪除失敗：{exc}")
else:
    st.sidebar.info("目前尚無監控飯店")

if st.sidebar.button("🔄 立即同步最新市場數據"):
    if not os.path.exists(DB_PATH):
        st.sidebar.error("資料庫尚未建立，請先執行 main.py。")
    else:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        try:
            subprocess.run([sys.executable, script_path], cwd=os.path.dirname(os.path.abspath(__file__)), check=True)
            st.sidebar.success("同步完成，頁面將重新整理。")
            st.rerun()
        except subprocess.CalledProcessError:
            st.sidebar.error("同步失敗：main.py 返回錯誤。")
        except Exception as exc:
            st.sidebar.error(f"同步執行失敗：{exc}")

st.title("🏨 AI 動態房價決策中心")

if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM room_performance", conn)

        if monitored_hotels:
            if 'hotel_name' in df.columns:
                df = df[df['hotel_name'].isin(monitored_hotels)]
        else:
            df = df.iloc[0:0]

        if not df.empty:
            for col in ['ota_price', 'google_search_volume', 'is_main_room_type', 'suggested_price', 'price_delta']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            display_df = df.drop(columns=['id'], errors='ignore').rename(columns={
                "date": "日期", "hotel_name": "飯店名稱", "room_type": "房型",
                "ota_price": "OTA 售價", "google_search_volume": "搜尋熱度",
                "is_main_room_type": "是否主力", "suggested_price": "建議售價",
                "price_delta": "價格偏差值", "strategy_note": "策略建議"
            })
            display_df = display_df.dropna(subset=["價格偏差值", "策略建議"], how="all")

            col1, col2, col3 = st.columns(3)
            avg_price = df['ota_price'].mean() if 'ota_price' in df.columns else float('nan')
            max_price = df['ota_price'].max() if 'ota_price' in df.columns else float('nan')
            col1.metric("總資料筆數", len(df))
            col2.metric("平均 OTA 售價", f"{avg_price:.0f}" if not pd.isna(avg_price) else "N/A")
            col3.metric("今日最高售價", f"{max_price:.0f}" if not pd.isna(max_price) else "N/A")

            try:
                ota_df = pd.read_sql_query("SELECT * FROM ota_offers", conn)
                if not ota_df.empty:
                    if monitored_hotels and 'hotel_name' in ota_df.columns:
                        ota_df = ota_df[ota_df['hotel_name'].isin(monitored_hotels)]
                    ota_pivot = ota_df.pivot_table(index=['date', 'hotel_name', 'room_type'], columns='ota_name', values='ota_price')
                    st.subheader("📌 各 OTA 報價比較（相同 OTA 在同一欄）")
                    st.dataframe(ota_pivot.reset_index(), use_container_width=True)
            except Exception:
                pass

            st.subheader("📋 原始爬蟲與策略資料")
            st.dataframe(display_df, use_container_width=True)

            event_df = pd.read_sql_query(
                "SELECT event_name AS 事件, city AS 城市, event_date AS 活動日期, historical_avg_price_increase AS 歷史漲幅, MIN(created_at) AS 建立時間 FROM city_events WHERE city = '台中' AND event_date >= date('now') GROUP BY event_name, city, event_date ORDER BY event_date ASC LIMIT 5",
                conn
            )
            if not event_df.empty:
                st.subheader("🔔 最近市場事件")
                st.table(event_df)
        else:
            st.info("目前無數據，請點擊左側同步按鈕以載入數據。")
    except Exception as exc:
        st.error(f"資料讀取發生錯誤：{exc}")
    finally:
        try:
            conn.close()
        except Exception:
            pass
else:
    st.warning("資料庫尚未建立，請先執行 main.py。")
