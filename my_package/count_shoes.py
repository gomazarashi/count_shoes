import cv2
import numpy as np


def count_shoes(path: str) -> bool:
    # 画像を読み込む
    img = cv2.imread(path)
    # 画像をグレースケールに変換
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # しきい値を設定
    canny_low = 25
    canny_high = 100
    # エッジ検出
    img_canny = cv2.Canny(gray, canny_low, canny_high)

    # 局所的にしきい値を決定し二値化
    img_binary = cv2.adaptiveThreshold(
        img_canny, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2
    )

    # オープニング処理の回数を設定
    iterations = 2

    # カーネル
    kernel = np.array(
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0],
        ],
        np.uint8,
    )

    # オープニング処理
    img_opening = cv2.morphologyEx(
        img_binary, cv2.MORPH_OPEN, kernel, iterations=iterations
    )

    # 白黒反転
    img_opening = cv2.bitwise_not(img_opening)

    # 輪郭抽出
    contours, _ = cv2.findContours(
        img_opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )

    # 一定範囲の面積の輪郭のみを抽出
    min_area = 25000
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    max_area = 100000
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) < max_area]


    # 二値化画像、オープニング画像、輪郭画像を表示
    if len(contours) > 0:
        # 靴がある場合
        return True
    else:
        # 靴がない場合
        return False


if __name__ == "__main__":
    if count_shoes("shoes.png"):
        print("部室に人がいます")
    else:
        print("部室に人はいません")
