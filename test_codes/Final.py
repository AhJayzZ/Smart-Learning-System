import cv2
import mediapipe as mp
import numpy as np

# 文字辨識套件
import pytesseract
from re import A
import unicodedata
import string
import language_tool_python
from autocorrect import Speller

# 跳出視窗用的
import tkinter as tk
from tkinter import messagebox

# 自動糾正API
tool = language_tool_python.LanguageTool('en-US')
spell = Speller(lang='en')

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
list = [1]*63  # 宣告一個陣列，用來處存手指位置


class trigers:
    def __init__(self, list):
        self.list = list
        self.a = ((self.list[15]-self.list[0])**2 +
                  (self.list[16]-self.list[1])**2)**0.5   # 點5到點0距離
        self.b = ((self.list[27]-self.list[0])**2 +
                  (self.list[28]-self.list[1])**2)**0.5   # 點9到點0距離
        self.c = ((self.list[39]-self.list[0])**2 +
                  (self.list[40]-self.list[1])**2)**0.5   # 點13到點0距離
        self.d = ((self.list[51]-self.list[0])**2 +
                  (self.list[52]-self.list[1])**2)**0.5   # 點17到點0距離
        self.e = (((self.list[51]-self.list[15])**2 +
                  (self.list[52]-self.list[16])**2)**0.5)*1.2   # 點5到點17距離

    # 點與點之間的距離
    def distance(self, x1, y1, x2, y2):
        if max(self.a, self.b, self.c, self.d, self.e) == 0:
            return 1
        else:
            return (((x1-x2)**2+(y1-y2)**2)**0.5) / max(self.a, self.b, self.c, self.d, self.e)

    # 斜率
    def slope(self, x1, y1, x2, y2):
        if x2 == x1:
            return 1
        else:
            return (y2-y1)/(x2-x1)

    # 若大拇指伸直:True; 否則: False

    def thumb(self):
        # 離散程度
        thumb_dis_a = self.distance(
            self.list[12], self.list[13], self.list[6], self.list[7])
        thumb_dis_b = self.distance(
            self.list[9], self.list[10], self.list[6], self.list[7])

        # 拇指各點到線(兩端點連成的直線)的距離和
        m = self.slope(self.list[0], self.list[1],
                       self.list[12], self.list[13])    # 直線斜率
        # 直線參數: y=slope*x+b => b= y-slope*x
        b = (self.list[1]) - m*(self.list[0])
        def line(x, y): return abs(m*x-y+b)      # 直線方程
        point_to_line = 0  # 拇指各點到線的和
        for point in range(1, 5):  # 點
            if max(self.a, self.b, self.c, self.d, self.e) == 0:
                # 公式
                point_to_line += (line(self.list[3*point],
                                  self.list[3*point+1])/(m**2+1)**0.5)*100
            else:
                point_to_line += (line(self.list[3*point], self.list[3*point+1])/(
                    m**2+1)**0.5) / max(self.a, self.b, self.c, self.d, self.e)  # 公式

        if (thumb_dis_a+thumb_dis_b) > 0.67 and (point_to_line < 0.35):
            return True
        else:
            return False

    # 若食指伸直:True; 否則: False
    def index_finger(self):
        index_finger_dis_a = self.distance(
            self.list[24], self.list[25], self.list[15], self.list[16])
        index_finger_dis_b = self.distance(
            self.list[21], self.list[22], self.list[15], self.list[16])
        index_finger_dis_c = self.distance(
            self.list[18], self.list[19], self.list[15], self.list[16])

        # 食指各點到線(兩端點連成的直線)的距離和
        m = self.slope(self.list[3*5], self.list[3*5+1],
                       self.list[3*8], self.list[3*8+1])    # 直線斜率
        # 直線參數: y=slope*x+b => b= y-slope*x
        b = (self.list[3*5+1]) - m*(self.list[3*5])
        def line(x, y): return abs(m*x-y+b)      # 直線方程
        point_to_line = 0  # 拇指各點到線的和
        for point in range(6, 8):  # 點
            if max(self.a, self.b, self.c, self.d, self.e) == 0:
                # 公式
                point_to_line += (line(self.list[3*point],
                                  self.list[3*point+1])/(m**2+1)**0.5)*100
            else:
                point_to_line += (line(self.list[3*point], self.list[3*point+1])/(
                    m**2+1)**0.5) / max(self.a, self.b, self.c, self.d, self.e)  # 公式

        # 重複點問題
        if (index_finger_dis_a+index_finger_dis_b+index_finger_dis_c) < 0.3:
            return True
        # (index_finger_dis_a+index_finger_dis_b+index_finger_dis_c)>1 and
        if (index_finger_dis_a > index_finger_dis_b) and (index_finger_dis_b > index_finger_dis_c) and (point_to_line < 0.12):
            return True
        else:
            return False
    # 若中指伸直:True; 否則: False

    def middle_finger(self):
        middle_finger_dis_a = self.distance(
            self.list[36], self.list[37], self.list[27], self.list[28])
        middle_finger_dis_b = self.distance(
            self.list[33], self.list[34], self.list[27], self.list[28])
        middle_finger_dis_c = self.distance(
            self.list[30], self.list[31], self.list[27], self.list[28])

        # 中指各點到線(兩端點連成的直線)的距離和
        m = self.slope(self.list[3*9], self.list[3*9+1],
                       self.list[3*12], self.list[3*12+1])    # 直線斜率
        # 直線參數: y=slope*x+b => b= y-slope*x
        b = (self.list[3*9+1]) - m*(self.list[3*9])
        def line(x, y): return abs(m*x-y+b)      # 直線方程
        point_to_line = 0  # 拇指各點到線的和
        for point in range(10, 12):  # 點
            if max(self.a, self.b, self.c, self.d, self.e) == 0:
                # 公式
                point_to_line += (line(self.list[3*point],
                                  self.list[3*point+1])/(m**2+1)**0.5)*100
            else:
                point_to_line += (line(self.list[3*point], self.list[3*point+1])/(
                    m**2+1)**0.5) / max(self.a, self.b, self.c, self.d, self.e)  # 公式

        # (middle_finger_dis_a+middle_finger_dis_b+middle_finger_dis_c)>1.1 and
        if (middle_finger_dis_a > middle_finger_dis_b) and (middle_finger_dis_b > middle_finger_dis_c) and (point_to_line < 0.1) \
                and self.distance(self.list[0], self.list[1], self.list[9*3], self.list[9*3+1]) < self.distance(self.list[0], self.list[1], self.list[12*3], self.list[12*3+1]):
            return True
        else:
            return False
    # 若無名指伸直:True; 否則: False

    def ring_finger(self):
        ring_finger_dis_a = self.distance(
            self.list[48], self.list[49], self.list[39], self.list[40])
        ring_finger_dis_b = self.distance(
            self.list[45], self.list[46], self.list[39], self.list[40])
        ring_finger_dis_c = self.distance(
            self.list[42], self.list[43], self.list[39], self.list[40])

        # 無名指各點到線(兩端點連成的直線)的距離和
        m = self.slope(self.list[3*13], self.list[3*13+1],
                       self.list[3*16], self.list[3*16+1])    # 直線斜率
        # 直線參數: y=slope*x+b => b= y-slope*x
        b = (self.list[3*13+1]) - m*(self.list[3*13])
        def line(x, y): return abs(m*x-y+b)      # 直線方程
        point_to_line = 0  # 拇指各點到線的和
        for point in range(14, 16):  # 點
            if max(self.a, self.b, self.c, self.d, self.e) == 0:
                # 公式
                point_to_line += (line(self.list[3*point],
                                  self.list[3*point+1])/(m**2+1)**0.5)*100
            else:
                point_to_line += (line(self.list[3*point], self.list[3*point+1])/(
                    m**2+1)**0.5) / max(self.a, self.b, self.c, self.d, self.e)  # 公式

        # (ring_finger_dis_a+ring_finger_dis_b+ring_finger_dis_c) > 1.15 and
        if (ring_finger_dis_a > ring_finger_dis_b) and (ring_finger_dis_b > ring_finger_dis_c) and (point_to_line < 0.1) \
                and self.distance(self.list[0], self.list[1], self.list[13*3], self.list[13*3+1]) < self.distance(self.list[0], self.list[1], self.list[16*3], self.list[16*3+1]):
            return True
        else:
            return False

    # 若小拇指伸直:True; 否則: False
    def pinky(self):
        pinky_dis_a = self.distance(
            self.list[60], self.list[61], self.list[51], self.list[52])
        pinky_dis_b = self.distance(
            self.list[57], self.list[58], self.list[51], self.list[52])
        pinky_dis_c = self.distance(
            self.list[54], self.list[55], self.list[51], self.list[52])

        # 小拇指各點到線(兩端點連成的直線)的距離和
        m = self.slope(self.list[3*17], self.list[3*17+1],
                       self.list[3*20], self.list[3*20+1])    # 直線斜率
        # 直線參數: y=slope*x+b => b= y-slope*x
        b = (self.list[3*17+1]) - m*(self.list[3*17])
        def line(x, y): return abs(m*x-y+b)      # 直線方程
        point_to_line = 0  # 拇指各點到線的和
        for point in range(18, 20):  # 點
            if max(self.a, self.b, self.c, self.d, self.e) == 0:
                # 公式
                point_to_line += (line(self.list[3*point],
                                  self.list[3*point+1])/(m**2+1)**0.5)*100
            else:
                point_to_line += (line(self.list[3*point], self.list[3*point+1])/(
                    m**2+1)**0.5) / max(self.a, self.b, self.c, self.d, self.e)  # 公式

        # (pinky_dis_a+pinky_dis_b+pinky_dis_c) > 0.9 and
        if (pinky_dis_a+pinky_dis_b+pinky_dis_c) > 0.9 and (pinky_dis_a > pinky_dis_b) and (pinky_dis_b > pinky_dis_c) and (point_to_line < 0.15) \
                and self.distance(self.list[0], self.list[1], self.list[17*3], self.list[17*3+1]) < self.distance(self.list[0], self.list[1], self.list[20*3], self.list[20*3+1]):
            return True
        else:
            return False

    # 顯示數字
    def some_pose(self):
        if not self.index_finger() and not self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "ZERO", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "ONE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "TWO", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and not self.thumb() and self.ring_finger() and not self.pinky():
            cv2.putText(image, "THREE", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and not self.thumb() and self.ring_finger() and self.pinky():
            cv2.putText(image, "FOUR", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and self.thumb() and self.ring_finger() and self.pinky():
            cv2.putText(image, "FIVE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if not self.index_finger() and not self.middle_finger() and self.thumb() and not self.ring_finger() and self.pinky():
            cv2.putText(image, "SIX", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "SEVEN", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "EIGHT", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and self.middle_finger() and self.thumb() and self.ring_finger() and not self.pinky():
            cv2.putText(image, "NINE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and self.thumb() and not self.ring_finger() and self.pinky():
            cv2.putText(image, "ROCK", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 255), 2, cv2.LINE_AA)
        if not self.index_finger() and not self.middle_finger() and self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "Good Game", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)


state = False
show = False
do_it = False
error_tolerance = 0

# For webcam input:
cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.2, min_tracking_confidence=0.2, max_num_hands=1) as hands:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_RGB2BGR)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # 顯示手部特徵點

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # cv2.COLOR_BGR2GRAY
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # 用一個長度為63的矩陣，儲存21個手的特徵點(x,y,z)
                # 排序方式為[ 0的x,y,z; 1的x,y,z...]
                for i in range(21):
                    list[3*i] = float(hand_landmarks.landmark[i].x)
                    list[3*i+1] = float(hand_landmarks.landmark[i].y)
                    list[3*i+2] = float(hand_landmarks.landmark[i].z)

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        triger = trigers(list)
        triger.some_pose()
        # 測試

        # 給手部辨識一個容錯的範圍
        if triger.index_finger() and not triger.middle_finger() and not triger.ring_finger() and not triger.thumb() and not triger.pinky():
            do_it = True
            error_tolerance = 0
        else:
            error_tolerance += 1

        if error_tolerance > 3:
            do_it = False

        # 當食指滑過，擷取圖片
        if not state and do_it:
            show = False
            initial_poistion_w = int(
                list[3*8]*float(image.shape[1]))       # 初始食指x位置
            initial_poistion_h = int(
                list[3*8+1]*float(image.shape[0]))    # 初始食指y位置
            # print(initial_poistion_h)
            state = True
        elif state and do_it:
            now_w = int(list[3*8]*float(image.shape[1]))      # 手指滑動時，食指x位置
            now_h = int(list[3*8+1]*float(image.shape[0]))   # 手指滑動時，食指y位置
            cv2.rectangle(image, (initial_poistion_w, initial_poistion_h),
                          (now_w, now_h), (255, 105, 65), 2)
            # print("state= ",state)
        else:
            if state:
                final_w = int(list[3*8]*float(image.shape[1]))      # 結束時，食指x位置
                final_h = int(list[3*8+1]*float(image.shape[0]))   # 結束時，食指y位置
                state = False
                show = True
            if show:
                show = False
                cv2.rectangle(image, (initial_poistion_w, initial_poistion_h),
                              (final_w, final_h), (0, 255, 255), 2)

                if (initial_poistion_h > final_h):
                    initial_poistion_h, final_h = final_h, initial_poistion_h
                if initial_poistion_w > final_w:
                    initial_poistion_w, final_w = final_w, initial_poistion_w

                # 擷取圖片
                crop_img = image[initial_poistion_h: final_h,
                                 initial_poistion_w:final_w]
                crop_img_copy = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
                crop_img_copy = cv2.medianBlur(
                    crop_img_copy, 3)    # 除噪(降低邊緣雜訊)
                average_of_image = np.mean(crop_img_copy)  # 計算圖片平均灰度
                th3 = cv2.adaptiveThreshold(
                    crop_img_copy, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)    # 自適應二值化
                th3 = cv2.medianBlur(th3, 3)
                cv2.imshow("自適應二值化", th3)

                if average_of_image > 100 and average_of_image < 180:
                    # your code
                    # --------------------------------------------------------------------------------------------------------------------------------------------------
                    # 白名單設定(來自別人github)
                    valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
                    char_limit = 10000

                    def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
                        # replace spaces
                        for r in replace:
                            filename = filename.replace(r, ' ')

                        # keep only valid ascii chars
                        cleaned_filename = unicodedata.normalize(
                            'NFKD', filename).encode('ASCII', 'ignore').decode()

                        # keep only whitelisted chars
                        cleaned_filename = ''.join(
                            c for c in cleaned_filename if c in whitelist)
                        if len(cleaned_filename) > char_limit:
                            print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(
                                char_limit))
                        return cleaned_filename[:char_limit]
                    # -------------------------------------------------------------------------------------------------------------------------------------------
                    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
                    text = pytesseract.image_to_string(
                        th3, lang='eng')     # 抓取文字

                    # 將文字儲存成文字檔
                    with open("file.txt", "a", encoding="utf-8") as file:

                        # 文字糾正API; tool.correct()
                        file.write(tool.correct(clean_filename(text)))
                        file.write("\n\n\n")
                '''
                # 光線太亮
                elif average_of_image <= 100:
                    # 跳出視窗警告
                    root = tk.Tk()
                    root.withdraw()
                    # 括號裡面的兩個字串分別代表彈出視窗的標題(title)與要顯示的文字(index)
                    messagebox.showinfo("警告", "光線太亮")

                # 光線不足
                else:
                    # 跳出視窗警告
                    root = tk.Tk()
                    root.withdraw()
                    # 括號裡面的兩個字串分別代表彈出視窗的標題(title)與要顯示的文字(index)
                    messagebox.showinfo("警告", "光線不足")
                '''
        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
