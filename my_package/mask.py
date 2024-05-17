#受け取った画像にmask処理を行う
import cv2

def mask(img_path:str,mask_path:str)->str:
    #画像の読み込み
    img=cv2.imread(img_path)
    mask=cv2.imread(mask_path,0)
    #mask処理
    img_masked=cv2.bitwise_and(img,img,mask=mask)
    #画像の保存
    cv2.imwrite(f'{img_path.removesuffix(".png")}_masked.png',img_masked)
    
if __name__ == '__main__':
    mask('shoes_2.png','mask.png')