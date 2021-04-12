import cv2
import pytesseract
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread('IMG_20210412_162604.jpg',0) # 轉灰階
image = cv2.medianBlur(image, 5)    # 除噪(使圖片清晰)
ret, th1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)    #  一般二值化
th3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)    # 自適應二值化(自適應高斯閾值)
text = pytesseract.image_to_string(th3, lang='eng')     # 抓取文字

# 將文字儲存成文字檔
with open ("im_to_string2.txt", "w",encoding="utf-8") as file:
        file.write(text)

# 顯示圖片      
images=[image,th1,th3]
titles=["Original Image","Global Thresholding (v = 127)","Adaptive Gaussian Thresholding"]

for i in range(3):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()




