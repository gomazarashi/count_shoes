import cv2
from datetime import datetime
from os.path import join, dirname  # ファイルのパスを取得するために使用

DEV_ID = 0

# 解像度の設定
WIDTH = 1920
HEIGHT = 1080

def get_image():
    cap = cv2.VideoCapture(DEV_ID)

    # 解像度の設定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    ret, frame = cap.read()

    if ret:
        # ファイル名に日付を指定
        date = datetime.now().strftime("%Y%m%d_%H%M%S")
        # カレントディレクトリにある「saved_images」フォルダに保存
        file_name = f"saved_images/{date}.jpg"
        cv2.imwrite(file_name, frame)
        
    cap.release()
    cv2.destroyAllWindows()
    return 

if __name__ == "__main__":
    get_image()
    print("画像を保存しました")
    print("saved_imagesフォルダを確認してください")
    
    