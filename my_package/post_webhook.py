# Webhookを用いて画像をDiscordに送信するプログラム
from dotenv import load_dotenv  # 環境変数を読み込むためのライブラリ
import os
from os.path import join, dirname  # ファイルのパスを扱うためのライブラリ
from discordwebhook import Discord

dotenv_path = join(dirname(__file__), "../.env")  # 環境変数を読み込む
load_dotenv(dotenv_path)

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")  # 環境変数からDISCORD_WEBHOOK_URLを取得

discord = Discord(url=DISCORD_WEBHOOK_URL)

def post_text_wh(content="メッセージ送信テスト"):
    discord.post(content=content)
    return

def post_image_wh(from_folder,image):
    image_path=from_folder+"/"+image
    discord.post(
    file={
        "file1": open(image_path, "rb"),
    },
)
    return

def main():
    image_path = "saved_images/image.jpg"
    print(image_path)
    post_image_wh(image_path)
    
if __name__ == "__main__":
    main()
    