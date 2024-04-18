import os
from my_package.get_filename_list import get_filename_list
from my_package.get_image import get_image
from my_package.post_webhook import post_text_wh, post_image_wh
import shutil  # ファイル移動用
from time import sleep  # スリープ用
from datetime import datetime  # 現在時刻取得用
from PIL import Image


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
    now = datetime.now()
    # 月曜日～土曜日の8:30あるいは日曜日の9:30に実行(画像送信開始)
    if ((now.weekday() < 6) and (now.hour == 8 and now.minute == 30)) or (
        (now.weekday() == 6) and (now.hour == 9 and now.minute == 30)
    ):
        start_job()
    # 月曜日～土曜日の22:00あるいは日曜日の18:00に実行(画像送信終了)
    elif ((now.weekday() < 6) and (now.hour == 22 and now.minute == 0)) or (
        (now.weekday() == 6) and (now.hour == 18 and now.minute == 0)
    ):
        end_job()
    # それ以外の時間は通常の画像送信
    else:
        post_images()


if __name__ == "__main__":
    main()
