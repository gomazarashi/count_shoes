# Webhookを用いて画像をDiscordに送信するプログラム
from dotenv import load_dotenv  # 環境変数を読み込むためのライブラリ
import os
from os.path import join, dirname  # ファイルのパスを扱うためのライブラリ
import requests  # HTTPリクエストを送信するためのライブラリ
import json  # JSONを扱うためのライブラリ


dotenv_path = join(dirname(__file__), ".env")  # 環境変数を読み込む
load_dotenv(dotenv_path)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # 環境変数からWEBHOOK_URLを取得

def post_text_wh(content="メッセージ送信テスト"):
    main_content = {"username": "bot", "content": content}

    headers = {"Content-Type": "application/json"}  # ヘッダーの設定

    response = requests.post(
        WEBHOOK_URL, json.dumps(main_content), headers=headers
    )  # メッセージを送信
    return

def post_image_wh(image_path,content="画像を送信します"):
    embeds = [
        {"image": {"url": image_path}},
    ]

    main_content = {"username": "bot", 
                    "content": content,
                    "embeds": embeds}

    headers = {"Content-Type": "application/json"}  # ヘッダーの設定

    response = requests.post(
        WEBHOOK_URL, json.dumps(main_content), headers=headers
    )  # メッセージを送信
    return

def main():
    image_path = "https://upload.wikimedia.org/wikipedia/commons/0/0b/Cat_poster_1.jpg"
    post_image_wh(image_path)
    
if __name__ == "__main__":
    main()
    