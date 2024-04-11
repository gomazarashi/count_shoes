#RoboflowのAPIを利用して、靴を認識した際の画像と靴の数を返すプログラム
from dotenv import load_dotenv  # 環境変数を読み込むためのライブラリ
import os
from os.path import join, dirname  # ファイルのパスを扱うためのライブラリ

from roboflow import Roboflow
import supervision as sv
import cv2
from PIL import Image

dotenv_path = join(dirname(__file__), "../.env")  # 環境変数を読み込む
load_dotenv(dotenv_path)

ROBOFLOW_API_KEY=os.environ.get("ROBOFLOW_API_KEY")

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace().project("amr_shoes") 
model = project.version(2).model 

def count_shoes_in_image(path: str) -> tuple:
    result = model.predict(path, confidence=40, overlap=80).json() #confidenceは信頼度、overlapは重複度
    labels = [item["class"] for item in result["predictions"]]
    detections = sv.Detections.from_inference(result)
    detections = detections[detections.class_id == 0]
    label_anotator = sv.LabelAnnotator()
    box_annotator = sv.BoundingBoxAnnotator()
    
    image=cv2.imread(path)
    
    annotated_image = box_annotator.annotate(scene=image, detections=detections)
    
    annotated_image=label_anotator.annotate(scene=annotated_image, detections=detections, labels=labels)
    
    #靴の数(1足につき2)
    num_shoes = len(detections)
    return annotated_image, num_shoes

if __name__ == "__main__":
    annotated_image,num_shoes = count_shoes_in_image("image.jpg")
    Image.fromarray(annotated_image).save("annotated_image.jpg")
    print(num_shoes)
