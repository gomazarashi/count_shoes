import os
from os.path import join, dirname
from get_images_list import get_images_list
from post_webhook import post_text_wh, post_image_wh
from get_image import get_image
import shutil
from time import sleep
import locale # ロケール設定用

# ロケール設定
locale.setlocale(locale.LC_ALL, 'ja_JP')

def move_image(image):
    try:
        shutil.move(f"saved_images/{image}", f"posted_images/{image}")
    except Exception as e:
        print(f"画像の移動中にエラーが発生しました: {e}")
        

def main():
    post_text_wh("メッセージの送信を開始します")
    get_image()
    images_list=get_images_list("saved_images")
    for image in images_list:
        post_image_wh(f"saved_images/{image}")
        sleep(5)
        move_image(image)
    post_text_wh("メッセージの送信を終了します")

        
if __name__ == "__main__":
    main()
    


