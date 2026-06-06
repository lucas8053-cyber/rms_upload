# mapper.py
def map_room_type(raw_name):
    name = raw_name.lower()
    if "suite" in name: return "套房"
    if "deluxe" in name: return "豪華房"
    if "superior" in name: return "高級房"
    if "twin" in name: return "雙床房"
    if "double" in name: return "大床房"
    if "standard" in name: return "標準房"
    return "其他"
