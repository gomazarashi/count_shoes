import os 
from os.path import join, dirname

# imagesフォルダ内の画像ファイル名を取得
def get_images_list():
    # imagesフォルダのパスを取得
    images_dir = join(dirname(__file__), "images")
    # imagesフォルダ内のファイル名を取得
    images_list = os.listdir(images_dir)
    return images_list

def main():
    print(get_images_list())  # ['image1.jpg', 'image2.jpg', 'image3.jpg']
    
if __name__ == "__main__":
    main()
