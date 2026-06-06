# mapper.py
def map_room_type(raw_name):
    # 若 API 傳回的是 Standard，我們保留它；但如果未來 API 變豐富，邏輯會自動生效
    return str(raw_name) if raw_name else "Standard"
