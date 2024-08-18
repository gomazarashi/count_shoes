from ultralytics import YOLO


def count_heads(image_path: str) -> int:
    model = YOLO("./best.pt")
    results = model(image_path)
    head_count = len(results[0].boxes)
    return head_count


if __name__ == "__main__":
    head_count = count_heads("shoes.jpg")
    print(f"部室にいるのは{head_count}人です")
