import cv2
import mediapipe as mp
import numpy as np

from finger_trigger import finger_trigger

from show_text_handler import show_text_handler
from crop_img_handler import crop_img_handler
from show_ROI_handler import show_ROI_handler

from text_recognition import text_recognition
from text_correction import text_correction

import STATE

'''# 跳出視窗用的
import tkinter as tk
from tkinter import messagebox'''

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

list = [1]*63  # 宣告一個陣列，用來處存手指位置

state_recognition = STATE.DO_NOTHING


def do_change_state_recognition(state_recognition, only_index_finger, only_indexNmiddle_finger):
    if (state_recognition == STATE.DO_NOTHING):
        if only_index_finger:
            state_recognition = STATE.START_CROP
        else:
            state_recognition = STATE.DO_NOTHING

    elif(state_recognition == STATE.START_CROP):
        state_recognition = STATE.CROPPING

    elif(state_recognition == STATE.CROPPING):
        if only_indexNmiddle_finger:
            state_recognition = STATE.CROPPING
        else:
            state_recognition = STATE.END_CROP

    elif(state_recognition == STATE.END_CROP):
        if only_indexNmiddle_finger:
            state_recognition = STATE.END_CROP
        else:
            state_recognition = STATE.GET_IMAGE

    elif(state_recognition == STATE.GET_IMAGE):
        state_recognition = STATE.DO_NOTHING

    return state_recognition


position_x_initial = 0
position_y_initial = 0
position_x_final = 0
position_y_final = 0

error_tolerance = 0

# For webcam input:
DEFAULT_CAMERA = 0
cap = cv2.VideoCapture(DEFAULT_CAMERA)
mp_drawing_styles = mp.solutions.drawing_styles

with mp_hands.Hands(
        min_detection_confidence=0.75,
        min_tracking_confidence=0.75,
        max_num_hands=1) as hands:
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
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        thumb, index_finger, middle_finger, ring_finger, pinky = finger_trigger(
            list)
        only_index_finger = (index_finger) and not (
            thumb and middle_finger and ring_finger and pinky)
        only_indexNmiddle_finger = (index_finger and middle_finger) and not (
            thumb and ring_finger and pinky)

        state_recognition = do_change_state_recognition(
            state_recognition, only_index_finger, only_indexNmiddle_finger)

        show_text_handler(image, state_recognition)

        # 給手部辨識一個容錯的範圍
        MAX_ERROR_TOLERANCE = 3
        if (state_recognition == STATE.CROPPING):
            if(error_tolerance < MAX_ERROR_TOLERANCE):
                error_tolerance = error_tolerance
            else:
                error_tolerance = 0
        else:
            if(error_tolerance < MAX_ERROR_TOLERANCE):
                error_tolerance = error_tolerance + 1
            else:
                error_tolerance = 0

        image.flags.writeable = False
        [position_x_initial, position_y_initial, position_x_final, position_y_final] = show_ROI_handler(
            image,
            state_recognition,
            [position_x_initial, position_y_initial, position_x_final, position_y_final])

        crop_img = image[position_y_initial: position_y_final,
                         position_x_initial: position_x_final]
        crop_img_new = crop_img_handler(crop_img)
        cv2.imshow("自適應二值化", crop_img_new)
        average_of_image = np.mean(crop_img)  # 計算圖片平均灰度
        '''if average_of_image > 100 and average_of_image < 180:
                text = text_recognition(th3)
                text = text_correction(text)
                # 將文字儲存成文字檔
                with open("file.txt", "a", encoding="utf-8") as file:
                    file.write(text)
                    file.write("\n\n\n")'''
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
