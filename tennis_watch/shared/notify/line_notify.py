import os
import requests
from dotenv import load_dotenv
from shared.config import settings

load_dotenv()

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")
USER_ID = os.getenv("USER_ID")


def send_line_message(message: str):
    """LINE送信。SEND_LINE=Falseのときはログだけ出す。"""
    if not settings.SEND_LINE:
        print("（設定）LINE送信OFF：通知は飛ばさない。")
        print("送信メッセージ（参考）:\n", message)
        return

    if not CHANNEL_ACCESS_TOKEN or not USER_ID:
        print("LINE の環境変数が設定されていない（CHANNEL_ACCESS_TOKEN / USER_ID）")
        return

    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
    }
    data = {
        "to": USER_ID,
        "messages": [{"type": "text", "text": message}],
    }

    r = requests.post(url, headers=headers, json=data, timeout=30)
    print("LINE Status:", r.status_code, "Response:", r.text)