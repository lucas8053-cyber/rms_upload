# mapper.py
def map_room_type(raw_name):
    name = str(raw_name).lower() if raw_name else ""
    
    # 針對房型名稱的關鍵字匹配
    if any(x in name for x in ["suite", "套房"]): return "Suite"
    if any(x in name for x in ["deluxe", "豪華", "premium"]): return "Deluxe"
    if any(x in name for x in ["superior", "高級"]): return "Superior"
    if any(x in name for x in ["twin", "雙床"]): return "雙床房"
    if any(x in name for x in ["double", "king", "大床"]): return "大床房"
    if any(x in name for x in ["standard", "classic", "single", "基本", "標準"]): return "Standard"
    
    return "Standard" # 預設值
