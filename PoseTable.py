#pose_table
from cv2 import cv2
import numpy as np
import mediapipe as mp
from PIL import Image
import pytesseract


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

def table(image,image_proto,hand_landmarks,start_count,start_x,start_y) :
    image_height, image_width, _ = image.shape
    #print(image.shape)
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
        for now_finger in range (0,5) :
            single_count = 0
            single_finger_sum_x,single_finger_sum_y=0,0
            for index_sum in range(1,5):
                single_finger_sum_x=single_finger_sum_x + image_width*hand_landmarks.landmark[4*(now_finger)+index_sum].x
                single_finger_sum_y=single_finger_sum_y + image_height*hand_landmarks.landmark[4*(now_finger)+index_sum].y
            single_finger_avg_x[now_finger]=single_finger_sum_x/4
            single_finger_avg_y[now_finger]=single_finger_sum_y/4
            cv2.circle(image,(int(single_finger_avg_x[now_finger]),int(single_finger_avg_y[now_finger])),10,(255,0,0),-1)
            for index in range(1,5):
                if ((abs(int(image_width*(hand_landmarks.landmark[4*(now_finger)+index].x)-single_finger_avg_x[now_finger])) < single_detect_length) &
                    (abs(int(image_height*(hand_landmarks.landmark[4*(now_finger)+index].y)-single_finger_avg_y[now_finger])) < single_detect_length)) :
                    single_count = single_count + 1
                if single_count == 4 :
                    #print("success")
                    finger_detected[now_finger] = 1
            
        #for test in range(0,5) :
           # print("INDEX:",test,"Detected:",finger_detected[test])

        #手勢判斷
        detected_length=50                     #判定手指與重心點長度   
        if (((pos_y4 < pos_y3) & (pos_y4 < int(image_height * hand_landmarks.landmark[0].y))) or  #手朝上
            ((pos_x4 < pos_x3) & (pos_x4 < int (image_height* hand_landmarks.landmark[0].x))))  : #手朝左 
            if abs(pos_x4-avg_x) >= detected_length or abs(pos_y4-avg_y) >= detected_length :
                finger_detected[FINGER] = 1
         
        elif (((pos_y4 > pos_y3) & (pos_y4 > int(image_height * hand_landmarks.landmark[0].y))) or #手朝下
            ((pos_x4 > pos_x3) & (pos_x4 > int (image_height* hand_landmarks.landmark[0].x)))):    #手朝右
            if abs(pos_x4-avg_x) >= detected_length or abs(pos_y4-avg_y) >= detected_length :
                finger_detected[FINGER] = 1
       
    ROI_x,ROI_y=(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)),
                    int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)))
        
    #TWO(兩隻手指頭)
    if start_count < 20 :
        ROI_x,ROI_y=(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)),
                    int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)))
        cv2.rectangle(image,(ROI_x,ROI_y-100),(ROI_x+100,ROI_y),(0,0,255),3)

        if finger_detected [2] & finger_detected[3] & ~finger_detected[1] & ~finger_detected[4] & ~finger_detected[5] :
            start_x,start_y = ROI_x,ROI_y
            start_count = start_count + 1
    else :
        cv2.putText(image,"Start Catching",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.rectangle(image,(start_x,start_y),(ROI_x,ROI_y),(0,0,255),3)
        if finger_detected[2] & ~finger_detected[3] :   #終止手勢
            start_count = 0
            #裁切圖片
            if (ROI_x < start_x) & (ROI_y < start_y)   :  #左上
                crop_image=image_proto[ROI_y:start_y,ROI_x:start_x]
            elif (ROI_x > start_x) & (ROI_y < start_y) :  #右上
                crop_image=image_proto[ROI_y:start_y,start_x:ROI_x]
            elif (ROI_x < start_x) & (ROI_y > start_y) :  #左下
                crop_image=image_proto[start_y:ROI_y,ROI_x:start_x]
            elif (ROI_x > start_x) & (ROI_y > start_y) :  #右下
                crop_image=image_proto[start_y:ROI_y,start_x:ROI_x]

            crop_image_height,crop_image_weight,_=crop_image.shape
            if(crop_image_height & crop_image_weight) :
                crop_image=cv2.flip(crop_image, 1)
                cv2.imshow("cropped image",crop_image)
                cv2.imwrite("output.png",crop_image)
                #Tesserat辨識文字
                img = Image.open("output.png")
                text=pytesseract.image_to_string(img, lang="eng")
                print(text)

                # 圖片二值化
                img_fix = Image.open('output.png')
                # 模式L”為灰色影象，它的每個畫素用8個bit表示，0表示黑，255表示白，其他數字表示不同的灰度。
                Img = img_fix.convert('L')
                Img.save("output_grayscale.png")
                # 自定義灰度界限，大於這個值為黑色，小於這個值為白色
                threshold = 50
                table = []
                for i in range(256):
                    if i < threshold:
                        table.append(0)
                    else:
                        table.append(1)
                # 圖片二值化
                photo = Img.point(table, '1')
                photo.save("output_binary.png")
                



    
    cv2.putText(image,"Finger Center Point:" + str((ROI_x,ROI_y)) ,(0,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    return center,ROI_x,ROI_y,start_count,start_x,start_y
    
   

#Conference:
    #if abs(int(image_height*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y-avg_y))) > 50 :
     # cv2.putText(image,"Index_y",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    #if abs(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].x-avg_x))) > 50 :
      #cv2.putText(image,"Index_x",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)