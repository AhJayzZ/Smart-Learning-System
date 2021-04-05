#pose_table
from cv2 import cv2
import mediapipe as mp

#PoseTableIndex:
  #WRIST = 0
  #THUMB_CMC = 1
  #THUMB_MCP = 2
  #THUMB_IP = 3
  #THUMB_TIP = 4
  #INDEX_FINGER_MCP = 5
  #INDEX_FINGER_PIP = 6
  #INDEX_FINGER_DIP = 7
  #INDEX_FINGER_TIP = 8
  #MIDDLE_FINGER_MCP = 9
  #MIDDLE_FINGER_PIP = 10
  #MIDDLE_FINGER_DIP = 11
  #MIDDLE_FINGER_TIP = 12
  #RING_FINGER_MCP = 13
  #RING_FINGER_PIP = 14
  #RING_FINGER_DIP = 15
  #RING_FINGER_TIP = 16
  #PINKY_MCP = 17
  #PINKY_PIP = 18
  #PINKY_DIP = 19
  #PINKY_TIP = 20


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def table(image,hand_landmarks,start,start_count,start_x,start_y) :
    start_count = start_count + 1
    image_height, image_width, _ = image.shape
    start_x,start_y=0,0
    detected_length=80                     #判定手指與重心點長度
    ROI_coef=1                              #給定ROI框的在上面或下面(預設上面:1)
    ROI_x,ROI_y=0,0                         #回傳的ROI中心點
    finger_detected=[0 for x in range(0,6)] #1:大拇指,2:食指,3:中指,4:無名指,5:小拇指
    single_finger_avg_x=[0 for x in range(0,6)]
    single_finger_avg_y=[0 for y in range(0,6)]


    #計算中心點座標和連結手部特徵點
    sum_x=0;sum_y=0
    for index in range(len(hand_landmarks.landmark)) :
      sum_x=sum_x+hand_landmarks.landmark[index].x
      sum_y=sum_y+hand_landmarks.landmark[index].y
    avg_x=int(sum_x/len(hand_landmarks.landmark) * image_width)
    avg_y=int(sum_y/len(hand_landmarks.landmark) * image_height)
    center=(avg_x,avg_y)
    cv2.circle(image,center,10,(255,0,0), -1)  


    for FINGER in range(1,6) :
        #指頭節點
        pos_x4=int(image_width * (hand_landmarks.landmark[4*FINGER].x))
        pos_y4=int(image_height * (hand_landmarks.landmark[4*FINGER].y))
        #次指頭節點
        pos_x3=int(image_width * (hand_landmarks.landmark[4*FINGER-1].x))
        pos_y3=int(image_height * (hand_landmarks.landmark[4*FINGER-1].y))


        #單點重複判斷
        single_detect_length = 20
        single_count = 0
        single_finger_sum_x,single_finger_sum_y=0,0
        for index in range(1,5):
            single_finger_sum_x=single_finger_sum_x + hand_landmarks.landmark[4*(FINGER-1)+index].x
            single_finger_sum_y=single_finger_sum_y + hand_landmarks.landmark[4*(FINGER-1)+index].y
        single_finger_avg_x[FINGER]=single_finger_sum_x/4
        single_finger_avg_y[FINGER]=single_finger_sum_y/4
        for index in range(1,5):
            if (abs(int(image_width*(hand_landmarks.landmark[4*(FINGER-1)+index].x-single_finger_avg_x[FINGER]))) < single_detect_length &
               abs(int(image_height*(hand_landmarks.landmark[4*(FINGER-1)+index].y-single_finger_avg_y[FINGER]))) < single_detect_length) :
                single_count = single_count + 1
            if single_count == 4 :
                print("success")
                finger_detected[FINGER] = 1


        #手勢判斷      
        if (pos_y4 < pos_y3) & (pos_y4 < int(image_height * hand_landmarks.landmark[0].y)) : #手翻上
            if abs(pos_x4-avg_x) >= detected_length or abs(pos_y4-avg_y) >= detected_length :
                finger_detected[FINGER] = 1
                ROI_coef = 1
        elif (pos_y4 > pos_y3) & (pos_y4 > int(image_height * hand_landmarks.landmark[0].y)) : #手翻下
            if abs(pos_x4-avg_x) >= detected_length or abs(pos_y4-avg_y) >= detected_length :
                finger_detected[FINGER] = 1
                ROI_coef = -1


        ROI_x,ROI_y=(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x)),
                    int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y)))
        
    #TWO(兩隻手指頭)
    if start_count <= 50 :
        start = 1
        start_x,start_y = ROI_x,ROI_y
        cv2.rectangle(image,(ROI_x,ROI_y-100),(ROI_x+200,ROI_y),(0,0,255),5)
        start_count = start_count + 1
    else :
        cv2.putText(image,"Starting",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.rectangle(image,(start_x,start_y),(ROI_x+200,ROI_y),(0,0,255),5)
        if finger_detected[2] & finger_detected[3] & finger_detected[4]:
            start_count = 0
            start = 0

    return center,ROI_coef,ROI_x,ROI_y,start_count,start_x,start_y
        




        # #擷取ROI圖片(.png)
        # if(ROI_x-200 > 50) & (ROI_x+200 <= image_width) :
        #     if(ROI_coef > 0 & ROI_y-ROI_coef*200 > 50 ) :
        #         crop_image=image[ROI_y-ROI_coef*200:ROI_y,ROI_x-200:ROI_x+200]
        #         cv2.imshow("cropped image",crop_image)
        #         cv2.imwrite("output.png",crop_image)
        #     elif (ROI_coef < 0 & ROI_y-ROI_coef*200 <= image_height ) :
        #         crop_image=image[ROI_y:ROI_y-ROI_coef*200,ROI_x-200:ROI_x+200]
        #         cv2.imshow("cropped image",crop_image)
        #         cv2.imwrite("output.png",crop_image)   
   

#Conference:
    #if abs(int(image_height*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y-avg_y))) > 50 :
     # cv2.putText(image,"Index_y",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    #if abs(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x-avg_x))) > 50 :
      #cv2.putText(image,"Index_x",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)