from re import A
import cv2
import pytesseract
import numpy as np
import unicodedata
import string
import language_tool_python
from autocorrect import Speller
# 跳出視窗用的
import tkinter as tk
from tkinter import messagebox


tool = language_tool_python.LanguageTool('en-US')
spell = Speller(lang='en')

# --------------------------------------------------------------------------------------------------------------------------------------------------
# 白名單設定(來自別人github)
valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit =10000
def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,' ')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    

#-------------------------------------------------------------------------------------------------------------------------------------------

# 讀取圖片
image = cv2.imread('test3.jpg',0) 
image = cv2.medianBlur(image, 5)    # 除噪(使圖片清晰)(中值慮波)
image_copy = image.copy()


average_of_image = np.mean(image_copy) # 計算圖片平均灰度


if average_of_image > 100 and average_of_image < 180:
    print("1")
    th3 = cv2.adaptiveThreshold(image_copy, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)    # 自適應二值化(自適應高斯閾值)
    th3 = cv2.medianBlur(th3, 3)  # 除噪(使圖片清晰)(中值慮波)
    text = pytesseract.image_to_string(th3, lang='eng')     # 抓取文字

    # 將文字儲存成文字檔
    with open ("im_to_string1.txt", "a",encoding="utf-8") as file:
        file.write(tool.correct(clean_filename(text))) # 文字糾正API; tool.correct()
        file.write("\n\n\n")

elif average_of_image <=100 :
    # 跳出視窗警告
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("警告", "光線太亮")
else: 
    # 跳出視窗警告
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("警告", "光線不足")
