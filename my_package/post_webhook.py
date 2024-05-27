# Webhookを用いて画像やテキストをDiscord/Slackに送信するプログラム
from dotenv import load_dotenv  # 環境変数を読み込むためのライブラリ
import os
from os.path import join, dirname  # ファイルのパスを扱うためのライブラリ
from discordwebhook import Discord
import requests
import json

dotenv_path = join(dirname(__file__), "../../env_dir/.env")  # 環境変数を読み込む
load_dotenv(dotenv_path)

# 環境変数からDISCORD_WEBHOOK_URLを取得
DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# 環境変数からSLACK_WEBHOOK_URLを取得
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")


discord = Discord(url=DISCORD_WEBHOOK_URL)


def post_text_discord(content="メッセージ送信テスト"):
    discord.post(content=content)
    return


def post_image_discord(from_folder, image):
    image_path = from_folder + "/" + image
    discord.post(
        file={
            "file1": open(image_path, "rb"),
        },
    )
    return


def post_text_slack(user_name="テスト", content="メッセージ送信テスト"):
    post_json = {
        "username": user_name,
        "text": content,
    }
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(post_json))


def main():
    post_text_slack()


if __name__ == "__main__":
    main()
