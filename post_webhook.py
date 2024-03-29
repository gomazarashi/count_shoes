# Webhookを用いて画像をDiscordに送信するプログラム
from dotenv import load_dotenv  # 環境変数を読み込むためのライブラリ
import os
from os.path import join, dirname  # ファイルのパスを扱うためのライブラリ
from discordwebhook import Discord

dotenv_path = join(dirname(__file__), ".env")  # 環境変数を読み込む
load_dotenv(dotenv_path)

WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # 環境変数からWEBHOOK_URLを取得

discord = Discord(url=WEBHOOK_URL)

def post_text_wh(content="メッセージ送信テスト"):
    discord.post(content=content)
    return

def post_image_wh(image_path):
    discord.post(
    file={
        "file1": open(image_path, "rb"),
    },
)
    return

def main():
    image_path = "./saved_images/20240324_003502.jpg"
    print(image_path)
    post_image_wh(image_path)
    
if __name__ == "__main__":
    main()
    