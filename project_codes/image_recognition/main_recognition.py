import cv2
import mediapipe as mp
import numpy as np

from handedness_detector import get_handedness

from finger_trigger import if_only_index_finger, if_indexNmiddle_finger

from show_text_handler import show_text_handler
from crop_img_handler import crop_img_handler
from ROI_bound_handler import ROI_bound_handler

from text_recognition import text_recognition
from text_correction import text_correction

import STATE

import USER

# 用一個長度為63的矩陣，儲存21個手的特徵點(x,y,z)
# 排序方式為[ 0的x,y,z; 1的x,y,z...]


def get_list_point_hand(hand_landmarks):
    list_point_hand = [1]*63
    i = 0
    for landmark in hand_landmarks:
        list_point_hand[3 * i] = float(landmark.x)
        list_point_hand[3 * i + 1] = float(landmark.y)
        list_point_hand[3 * i + 2] = float(landmark.z)
        i = i + 1
    return list_point_hand


position_x_initial = 0
position_y_initial = 0
position_x_final = 0
position_y_final = 0

error_tolerance = 0

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles

state_recognition = STATE.WAIT_HANDEDNESS
last_state = state_recognition  # debug

# For webcam input:
DEFAULT_CAMERA = 0
cap = cv2.VideoCapture(DEFAULT_CAMERA)

with mp_hands.Hands(
        static_image_mode=False,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
        max_num_hands=1)as hands:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        else:
            # Flip the image horizontally for a later selfie-view display,
            # and convert the BGR image to RGB before processing.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # get handedness for match with user's handedness
            handedness = get_handedness(results.multi_handedness)

            # start state
            if(handedness == USER.HANDEDNESS):
                if(state_recognition == STATE.WAIT_HANDEDNESS):
                    state_recognition = STATE.WAIT_ONLY_INDEX_FINGER

                elif(state_recognition == STATE.WAIT_ONLY_INDEX_FINGER):
                    for hand_landmarks in results.multi_hand_landmarks:
                        list_point_hand = get_list_point_hand(
                            hand_landmarks.landmark)
                    only_index_finger = if_only_index_finger(list_point_hand)

                    if only_index_finger:
                        state_recognition = STATE.START_CROP
                    else:
                        state_recognition = STATE.WAIT_ONLY_INDEX_FINGER

                elif(state_recognition == STATE.START_CROP):
                    for hand_landmarks in results.multi_hand_landmarks:
                        list_point_hand = get_list_point_hand(
                            hand_landmarks.landmark)
                    position_x_initial, position_y_initial, position_x_final, position_y_final = ROI_bound_handler(
                        image,
                        state_recognition,
                        [position_x_initial, position_y_initial,
                         position_x_final, position_y_final],
                        list_point_hand)

                    state_recognition = STATE.CROPPING

                elif(state_recognition == STATE.CROPPING):
                    for hand_landmarks in results.multi_hand_landmarks:
                        list_point_hand = get_list_point_hand(
                            hand_landmarks.landmark)
                    position_x_initial, position_y_initial, position_x_final, position_y_final = ROI_bound_handler(
                        image,
                        state_recognition,
                        [position_x_initial, position_y_initial,
                         position_x_final, position_y_final],
                        list_point_hand)
                    # Draw the hand annotations on the image.
                    image.flags.writeable = True
                    # convert the RGB image to BGR back
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style())

                    show_text_handler(image, state_recognition)
                    cv2.rectangle(image, (position_x_initial, position_y_initial),
                                  (position_x_final, position_y_final), (255, 105, 65), 2)

                    only_indexNmiddle_finger = if_indexNmiddle_finger(
                        list_point_hand)

                    if only_indexNmiddle_finger:
                        state_recognition = STATE.END_CROP
                    else:
                        state_recognition = STATE.CROPPING

                elif(state_recognition == STATE.END_CROP):
                    for hand_landmarks in results.multi_hand_landmarks:
                        list_point_hand = get_list_point_hand(
                            hand_landmarks.landmark)
                    position_x_initial, position_y_initial, position_x_final, position_y_final = ROI_bound_handler(
                        image,
                        state_recognition,
                        [position_x_initial, position_y_initial,
                         position_x_final, position_y_final],
                        list_point_hand)

                    if(position_x_initial != position_x_final) and (position_y_initial != position_y_final):
                        state_recognition = STATE.GET_WORDS
                    else:
                        print("0 point croped image")
                        state_recognition = STATE.CROPPING

                elif(state_recognition == STATE.GET_WORDS):
                    crop_img = image[position_y_initial: position_y_final,
                                     position_x_initial: position_x_final]

                    crop_img = crop_img_handler(crop_img)
                    # cv2.imshow("自適應二值化", crop_img_new)
                    average_of_image = np.mean(crop_img)  # 計算圖片平均灰度

                    if average_of_image > 100 and average_of_image < 180:

                        text = text_recognition(crop_img)
                        text = text_correction(text)
                        print(text)
                        # 將文字儲存成文字檔
                        with open("file.txt", "a", encoding="utf-8") as file:
                            file.write(text)
                            file.write("\n\n\n")
                    # 光線太亮
                    elif average_of_image <= 100:
                        print("警告: 光線太亮")

                    # 光線不足
                    else:
                        print("警告: 光線不足")

                    state_recognition = STATE.WAIT_HANDEDNESS
            else:
                state_recognition = STATE.WAIT_HANDEDNESS

            # 給手部辨識一個容錯的範圍
            '''
            MAX_ERROR_TOLERANCE = 20
            if (state_recognition == STATE.CROPPING):
                if(error_tolerance < MAX_ERROR_TOLERANCE):
                    error_tolerance = error_tolerance
                else:
                    error_tolerance = 0
            else:
                if(error_tolerance < MAX_ERROR_TOLERANCE):
                    error_tolerance = error_tolerance + 1
                else:
                    error_tolerance = 0'''

            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imshow('MediaPipe Hands', image)
            # wait 1ms, and & 0xFF for complement to the key we want (ascii 27 = esc)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        if(last_state != state_recognition):
            last_state = state_recognition
            STATE.print_state(state_recognition)
cap.release()

cv2.destroyAllWindows()
