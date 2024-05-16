import cv2
import matplotlib.pyplot as plt
import numpy as np


def count_shoes(path: str) -> int:
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
    iterations = 1

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
    contours, hierarchy = cv2.findContours(
        img_opening, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )

    # 一定以上の面積の輪郭のみ残す
    area = 1000
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > area]

    # 輪郭描画
    img_contour = cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

    # 二値化画像、オープニング画像、輪郭画像を表示
    plt.figure(figsize=(18, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img_canny, cv2.COLOR_BGR2RGB))
    plt.title("Binary")
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(img_opening, cv2.COLOR_BGR2RGB))
    plt.title(f"オープニング処理\n回数: {iterations}")
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
    plt.title(f"Contour\n物体の数:{len(contours)}")
    plt.show()


if __name__ == "__main__":
    count_shoes("shoes_cut.jpg")
