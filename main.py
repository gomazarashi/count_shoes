import os
import shutil
from time import sleep
from datetime import datetime
from my_package.get_filename_list import get_filename_list
from my_package.get_image import get_image
from my_package.post_webhook import (
    post_text_discord,
    post_image_discord,
    post_text_slack,
)
from my_package.count_heads import count_heads


def ensure_directories_exist(directories: list) -> None:
    """指定されたディレクトリが存在しなければ作成します"""
    for directory in directories:
        if not os.path.exists(directory):
            os.mkdir(directory)


def clear_directory(directory: str) -> None:
    """ディレクトリ内の全てのファイルを削除します"""
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def move_image(from_folder: str, to_folder: str, image: str) -> None:
    """画像を指定されたフォルダに移動します"""
    try:
        shutil.move(os.path.join(from_folder, image), os.path.join(to_folder, image))
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")


def post_current_time() -> None:
    """現在の時刻をDiscordとSlackに投稿します"""
    current_time = datetime.now().strftime("%H:%M:%S")
    post_text_discord(f"現在の時刻は{current_time}です")
    post_text_slack("部室内人数通知システム", f"現在の時刻は{current_time}です")


def capture_and_process_image() -> None:
    """画像を撮影し、人数をカウントして結果を投稿します"""
    try:
        # 画像を撮影して保存
        get_image("shotten_images")

        # 画像のファイル名リストを取得
        images_list = get_filename_list("shotten_images")

        if not images_list:
            print("画像が存在しません")
            return

        image = images_list[0]
        
        post_current_time()

        # 画像をDiscordに投稿
        post_image_discord("shotten_images", image)

        # 人数をカウント
        count_heads_result = count_heads(
            os.path.join("shotten_images", image), "./my_package/best.pt"
        )

        # 画像を移動
        move_image("shotten_images", "posted_images", image)

        # 人数をDiscordとSlackに投稿
        post_text_discord(f"部室内の人数は{count_heads_result}人です")
        post_text_slack(
            "部室内人数通知システム", f"部室内の人数は{count_heads_result}人です"
        )

    except Exception as e:
        print(f"画像処理中にエラーが発生しました: {e}")


def start_job() -> None:
    """ジョブの開始を通知し、画像処理を実行します"""
    try:
        with open("./version.txt") as f:
            version = f.read()
        post_text_discord(f"現在のバージョンは{version}です\n画像の送信を開始します")
        post_text_slack(
            "部室内人数通知システム",
            f"現在のバージョンは{version}です\n画像の送信を開始します",
        )
        capture_and_process_image()
    except Exception as e:
        print(f"ジョブの開始中にエラーが発生しました: {e}")


def end_job() -> None:
    """ジョブの終了を通知し、画像処理を実行します"""
    try:
        capture_and_process_image()
        post_text_discord("画像の送信を終了します")
        post_text_slack("部室内人数通知システム", "画像の送信を終了します")
    except Exception as e:
        print(f"ジョブの終了中にエラーが発生しました: {e}")


def main() -> None:
    """メインの実行関数"""
    ensure_directories_exist(["shotten_images", "posted_images"])

    now = datetime.now().replace(second=0, microsecond=0)
    weekday = now.weekday()

    # 稼働時間の設定
    start_time = (
        now.replace(hour=8, minute=30)
        if weekday < 6
        else now.replace(hour=9, minute=30)
    )
    end_time = (
        now.replace(hour=22, minute=0)
        if weekday < 6
        else now.replace(hour=18, minute=0)
    )

    # 稼働時間に基づく処理
    if now < start_time or now > end_time:
        print("稼働時間外です")
    elif now == start_time:
        start_job()
    elif now == end_time:
        end_job()
    else:
        capture_and_process_image()


if __name__ == "__main__":
    main()
