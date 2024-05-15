import os
from my_package.get_filename_list import get_filename_list
from my_package.get_image import get_image
from my_package.post_webhook import post_text_wh, post_image_wh
import shutil  # ファイル移動用
from time import sleep  # スリープ用
from datetime import datetime  # 現在時刻取得用


def move_image(from_folder, to_folder, image):
    try:
        shutil.move(from_folder + "/" + image, to_folder + "/" + image)
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")


def post_current_time():
    current_time = datetime.now().strftime("%H:%M:%S")
    post_text_wh(f"現在の時刻は{current_time}です")


def post_images():
    get_image("saved_images")
    images_list = get_filename_list("saved_images")
    post_current_time()

    for image in images_list:
        post_image_wh("saved_images", image)
        sleep(1)
        move_image("saved_images", "posted_images", image)


def start_job():
    post_text_wh("画像の送信を開始します")
    post_images()


def end_job():
    post_text_wh("画像の送信を終了します")
    # posted_imagesフォルダの画像を削除
    shutil.rmtree("posted_images")
    os.mkdir("posted_images")


def main():
    # saved_imagesフォルダが存在しなければ作成
    if not os.path.exists("saved_images"):
        os.mkdir("saved_images")
    # posted_imagesフォルダが存在しなければ作成
    if not os.path.exists("posted_images"):
        os.mkdir("posted_images")
    now = datetime.now().replace(second=0, microsecond=0)  # 秒数は利用しないので0にする
    weekday = now.weekday()
    # 稼働時間の設定
    # 月曜日～土曜日
    if weekday < 6:
        # 開始時刻
        start_time = now.replace(hour=8, minute=30)
        # 終了時刻
        end_time = now.replace(hour=22, minute=0)
    # 日曜日
    else:
        # 開始時刻
        start_time = now.replace(hour=9, minute=30)
        # 終了時刻
        end_time = now.replace(hour=18, minute=0)
    
    # 稼働時間外
    if (now < start_time) or (end_time < now):
        print("稼働時間外です")
    # 稼働開始時刻
    elif now == start_time:
        start_job()
    # 稼働終了時刻
    elif now == end_time:
        end_job()
    # 通常の画像送信
    else:
        post_images()


if __name__ == "__main__":
    main()
