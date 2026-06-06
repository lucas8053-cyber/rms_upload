# mapper.py
def map_room_type(raw_name):
    name = str(raw_name).lower() if raw_name else ""
    
    # 核心邏輯：四級分級制
    if "suite" in name: return "Suite"
    if "deluxe" in name: return "Deluxe"
    if "superior" in name: return "Superior"
    if "standard" in name or "classic" in name or "single" in name: return "Standard"
    
    # 額外判斷：若名稱中有 Twin/Double 但不在上述級距，歸為 Standard
    if "twin" in name or "double" in name: return "Standard"
    
    return "Standard" # 預設歸類，確保無遺漏
