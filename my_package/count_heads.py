from ultralytics import YOLO
import math
import sys


def count_heads(image_path: str, model_path: str) -> int:
    model = YOLO(model_path)
    results = model(image_path)
    shoes_count = len(results[0].boxes)
    # 1人が2足の靴を持っていると仮定 端数切り上げ
    head_count = math.ceil(shoes_count / 2)
    return head_count


if __name__ == "__main__":
    # コマンドライン引数から画像ファイルパスを取得
    file_path = sys.argv[1]
    head_count = count_heads(file_path, "./best.pt")
    print(f"部室にいるのは{head_count}人です")
