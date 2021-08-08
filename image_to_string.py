# 陰影處理，提高辨識率
import cv2
import pytesseract
import numpy as np
import unicodedata
import string
import language_tool_python
from autocorrect import Speller

tool = language_tool_python.LanguageTool('en-US')
spell = Speller(lang='en')

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

image = cv2.imread('test3.jpg',0) 
image_copy = cv2.medianBlur(image, 5)    # 除噪(使圖片清晰)(中值慮波)

th3 = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)    # 自適應二值化(自適應高斯閾值)
th3 = cv2.medianBlur(image, 3)  # 除噪(使圖片清晰)(中值慮波)
text = pytesseract.image_to_string(th3, lang='eng')     # 抓取文字


# 將文字儲存成文字檔
with open ("im_to_string1.txt", "a",encoding="utf-8") as file:

    file.write(tool.correct(clean_filename(text))) # 文字糾正API; tool.correct()
    file.write("\n\n\n")

    










