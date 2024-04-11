import os 
from os.path import join, dirname

# 与えられたフォルダ内の画像ファイル名を取得
def get_filename_list(path):
    images_list = os.listdir(path)
    return images_list

def main():
    print(get_filename_list())  # ['image1.jpg', 'image2.jpg', 'image3.jpg']
    
if __name__ == "__main__":
    main()
