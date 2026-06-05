import os
import sys
# 確保這些模組在同一目錄下
from database_manager import init_db
from scraper import run_scraper
from analysis import calculate_and_update_strategy, check_for_events_and_alert

def start_system():
    # 1. 強制設定目錄
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"📂 系統運作路徑: {project_dir}")

    # 2. 資料庫初始化
    print("正在初始化資料庫...")
    init_db()
    
    # 3. 爬蟲
    print("正在執行爬蟲...")
    run_scraper()
    
    # 4. 分析與活動檢查
    print("正在執行房型績效分析...")
    calculate_and_update_strategy()
    
    print("正在檢查市場重大活動...")
    check_for_events_and_alert()
    
    print("✅ 系統循環執行完成")

if __name__ == "__main__":
    print("🚀 程式開始啟動...")
    start_system()