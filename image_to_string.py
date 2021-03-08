import cv2
import pytesseract
from PIL import Image

image = Image.open('im_process.png').convert('L')   #圖片轉灰階
for i in range(image.size[1]):  # '.size[1]'圖片高
    for j in range(image.size[0]):  # '.size[0]'圖片寬
        if image.getpixel((j,i))>128:   # 若RGB顏色比128淺，則直接將其改成白色。(測試結果)
            image.putpixel((j,i),255)
text = pytesseract.image_to_string(image, lang='chi_tra+eng')   
#print(text)


# 將文字儲存成文字檔
with open ("im_to_string2.txt", "w",encoding="utf-8") as file:
        file.write(text)
