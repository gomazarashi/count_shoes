import os
from os.path import join, dirname
from get_images_list import get_images_list
from get_image import get_image # 画像取得用
from post_webhook import post_text_wh, post_image_wh
import shutil # ファイル移動用
from time import sleep # スリープ用
import locale  # ロケール設定用
import datetime  # 現在時刻取得用
import schedule  # スケジュール実行用

# ロケール設定
locale.setlocale(locale.LC_ALL, "ja_JP")

def move_image(image):
    try:
        shutil.move(f"saved_images/{image}", f"posted_images/{image}")
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")

def post_images():
    get_image()
    images_list = get_images_list("saved_images")
    for image in images_list:
        post_image_wh("saved_images/"+image)
        sleep(1)
        move_image(image)


def start_job():
    post_text_wh("現在の時刻は"+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"です")
    post_text_wh("画像の送信を開始します")
    main_job()
    schedule.every(5).minutes.do(main_job)


def end_job():
    post_text_wh("現在の時刻は"+datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")+"です")
    post_text_wh("画像の送信を終了します")
    for job in schedule.jobs:
        if "main_job" in str(job):
            schedule.cancel_job(job)
            break
    #posted_imagesフォルダの画像を削除
    shutil.rmtree("posted_images")
    os.mkdir("posted_images")
    

#初回起動時に実行
def first_time():
    print("現在時刻: ", datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    print("「分」の値が5の倍数になるまで待機します。")        
    while True:
        now = datetime.datetime.now()
        if (now.minute % 5 == 0 and now.second == 0):
            print("これ以降、5分毎にメッセージを送信します。")
            start_job()
            break
        sleep(1)


def main_job():
    post_images()


def main():
    first_time()
    
    # 月曜日～土曜日の8:30～22:00の間に実行
    schedule.every().monday.at("08:30").do(start_job)
    schedule.every().monday.at("22:00").do(end_job)

    schedule.every().tuesday.at("08:30").do(start_job)
    schedule.every().tuesday.at("22:00").do(end_job)

    schedule.every().wednesday.at("08:30").do(start_job)
    schedule.every().wednesday.at("22:00").do(end_job)

    schedule.every().thursday.at("08:30").do(start_job)
    schedule.every().thursday.at("22:00").do(end_job)

    schedule.every().friday.at("08:30").do(start_job)
    schedule.every().friday.at("22:00").do(end_job)

    schedule.every().saturday.at("08:30").do(start_job)
    schedule.every().saturday.at("22:00").do(end_job)

    # 日曜日の9:30～18:00の間に実行
    schedule.every().sunday.at("09:30").do(start_job)
    schedule.every().sunday.at("18:00").do(end_job)
    
    
    
    while True:
        schedule.run_pending()
        sleep(1)

if __name__ == "__main__":
    main()


