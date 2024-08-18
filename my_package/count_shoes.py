from ultralytics import YOLO


if __name__ == "__main__":
    head_count = count_shoes("shoes.jpg")
    print("部室にいるのは{}人です".format(head_count))
