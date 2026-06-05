import requests

def send_telegram_msg(message):
    token = "你的_API_TOKEN"
    chat_id = "你的_CHAT_ID"
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)