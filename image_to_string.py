# 自適應二值化、侵蝕、膨脹、白名單 的文字辨識
import cv2
import pytesseract
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


image = cv2.imread('image.jpg',0) # 轉灰階
image = cv2.medianBlur(image, 5)    # 除噪(使圖片清晰)(中值慮波)
ret, th1 = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)    #  一般二值化
th3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)    # 自適應二值化(自適應高斯閾值)

# 侵蝕、膨脹
kernel = np.ones((3,3), np.uint8)
erosion = cv2.erode(th3, kernel, iterations = 1)    # 侵蝕
erosion = cv2.medianBlur(erosion, 13)
dilation = cv2.dilate(th3, kernel, iterations = 1)    # 膨脹
dilation= cv2.medianBlur(dilation, 3)


custom_config = r'-c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz --psm 6'
text = pytesseract.image_to_string(dilation, lang='eng',config=custom_config)     # 抓取文字  , config='--psm 6 sfz'
print(text)

# 將文字儲存成文字檔
with open ("file.txt", "w",encoding="utf-8") as file:
    file.write(text)

# 顯示圖片      
images=[image,th3,erosion,dilation]
titles=["Original Image","Adaptive Gaussian Thresholding","erosion","dilation"]

for i in range(4):
    plt.subplot(2, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()




