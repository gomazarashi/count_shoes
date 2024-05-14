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
    now = datetime.now()
    weekday = now.weekday()
    # 月曜日～土曜日
    if weekday < 6:
        # 稼働時間外
        if (
            (datetime.strptime("00:00:00", "%H:%M:%S") < now)
            and (now < datetime.strptime("08:30:00", "%H:%M:%S"))
            or (datetime.strptime("22:00:00", "%H:%M:%S") < now)
            and (now < datetime.strptime("23:59:59", "%H:%M:%S"))
        ):
            print("稼働時間外です")
        # 稼働開始時刻
        elif now == datetime.strptime("08:30:00", "%H:%M:%S"):
            start_job()
        # 稼働終了時刻
        elif now == datetime.strptime("22:00:00", "%H:%M:%S"):
            end_job()
        # 通常の画像送信
        else:
            post_images()
    # 日曜日
    else:
        # 稼働時間外
        if (
            (datetime.strptime("00:00:00", "%H:%M:%S") < now)
            and (now < datetime.strptime("09:30:00", "%H:%M:%S"))
            or (datetime.strptime("18:00:00", "%H:%M:%S") < now)
            and (now < datetime.strptime("23:59:59", "%H:%M:%S"))
        ):
            print("稼働時間外です")
        # 稼働開始時刻
        elif now == datetime.strptime("09:30:00", "%H:%M:%S"):
            start_job()
        # 稼働終了時刻
        elif now == datetime.strptime("18:00:00", "%H:%M:%S"):
            end_job()
        # 通常の画像送信
        else:
            post_images()


if __name__ == "__main__":
    main()
