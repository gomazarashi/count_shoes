import os
from os.path import join, dirname  # ファイルのパスを取得するために使用
from dotenv import load_dotenv  # 環境変数の読み込みに使用
import discord
from get_images_list import get_images_list

# .envファイルのパスを指定
dotenv_path = join(dirname(__file__), ".env")
# .envファイルの内容を読み込む
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
discord_client = discord.Client(intents=intents)

CHANNEL_ID = 1217780403327467611  # 画像投稿テスト用のチャンネルID


# botが起動した際、特定のチャンネルにメッセージを送信する
async def send_message():
    channel = discord_client.get_channel(CHANNEL_ID)
    await channel.send("botが起動しました")


# botが起動したときに実行されるイベント
@discord_client.event
async def on_ready():
    await send_message()


# チャンネル内で「!image」と発言した際に実行されるイベント
@discord_client.event
async def on_message(message):
    channel = message.channel
    if message.author.bot:
        return
    if message.content == "!image":
        images_list = get_images_list()
        for image in images_list:
            await channel.send(file=discord.File(f"images/{image}"))


# botを起動
discord_client.run(BOT_TOKEN)
