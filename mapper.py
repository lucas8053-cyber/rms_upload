# mapper.py
def map_room_type(raw_name):
    # 轉小寫處理
    name = str(raw_name).lower() if raw_name else ""
    
    if any(x in name for x in ["suite"]): return "套房"
    if any(x in name for x in ["deluxe", "premium"]): return "豪華房"
    if any(x in name for x in ["superior"]): return "高級房"
    if any(x in name for x in ["twin"]): return "雙床房"
    if any(x in name for x in ["double", "king", "queen"]): return "大床房"
    if any(x in name for x in ["standard", "classic", "single"]): return "標準房"
    
    return "標準房" # 預設歸類，避免顯示空值
