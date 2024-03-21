import os
from os.path import join, dirname
from dotenv import load_dotenv
import discord
from get_images_list import get_images_list
import shutil
import asyncio

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

BOT_TOKEN = os.environ.get("TOKEN")
intents = discord.Intents.default()
intents.typing = False
intents.message_content = True
discord_client = discord.Client(intents=intents)

CHANNEL_ID = 1217780403327467611


async def send_message():
    try:
        channel = discord_client.get_channel(CHANNEL_ID)
        await channel.send("botが起動しました")
    except Exception as e:
        print(f"メッセージの送信中にエラーが発生しました: {e}")


async def post_images():
    try:
        images_list = get_images_list("saved_images")
        for image in images_list:
            channel = discord_client.get_channel(CHANNEL_ID)
            await channel.send(file=discord.File(f"saved_images/{image}"))
            await move_image(image)
    except Exception as e:
        print(f"画像の投稿中にエラーが発生しました: {e}")


async def move_image(image):
    try:
        shutil.move(f"saved_images/{image}", f"posted_images/{image}")
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")


async def periodic_post():
    while True:
        await post_images()
        await asyncio.sleep(300)  # 5分ごとに実行


@discord_client.event
async def on_ready():
    await send_message()
    asyncio.create_task(
        periodic_post()
    )  # バックグラウンドタスクとしてperiodic_post()を実行


discord_client.run(BOT_TOKEN)
