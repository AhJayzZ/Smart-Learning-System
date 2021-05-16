#pose_table
from cv2 import cv2
import numpy as np
import mediapipe as mp
import pytesseract  
from PIL import Image
from googletrans import Translator

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

#---------------------------------------------------------------------------------
#計算中心點座標
def avg_point(image,hand_landmarks,image_height,image_width):
    sum_x=0;sum_y=0
    for index in range(len(hand_landmarks.landmark)) :
        sum_x=sum_x+hand_landmarks.landmark[index].x
        sum_y=sum_y+hand_landmarks.landmark[index].y
    avg_x=int(sum_x/len(hand_landmarks.landmark) * image_width)
    avg_y=int(sum_y/len(hand_landmarks.landmark) * image_height)
    center=(avg_x,avg_y)
    cv2.circle(image,center,10,(255,0,0), -1) 
    return avg_x,avg_y,center 

#---------------------------------------------------------------------------------
#單點重複判斷
def single_detected(image,hand_landmarks,finger_detected,image_height,image_width):
    single_detect_length = 10                   #單點重覆判斷距離
    single_finger_avg_x=[0 for x in range(0,6)]
    single_finger_avg_y=[0 for y in range(0,6)]
    for now_finger in range (0,5) :
        single_count ,single_finger_sum_x,single_finger_sum_y=0,0,0
        #計算五支手指頭的平均位置
        for index_sum in range(1,5):
            single_finger_sum_x=single_finger_sum_x + image_width*hand_landmarks.landmark[4*(now_finger)+index_sum].x
            single_finger_sum_y=single_finger_sum_y + image_height*hand_landmarks.landmark[4*(now_finger)+index_sum].y
        single_finger_avg_x[now_finger]=single_finger_sum_x/4
        single_finger_avg_y[now_finger]=single_finger_sum_y/4
        cv2.circle(image,(int(single_finger_avg_x[now_finger]),int(single_finger_avg_y[now_finger])),10,(255,0,0),-1)
        #檢測該手指所有節點是否都小於重覆判斷距離內
        for index in range(1,5):
            if ((abs(int(image_width*(hand_landmarks.landmark[4*(now_finger)+index].x)-single_finger_avg_x[now_finger])) < single_detect_length) &
                (abs(int(image_height*(hand_landmarks.landmark[4*(now_finger)+index].y)-single_finger_avg_y[now_finger])) < single_detect_length)) :
                single_count = single_count + 1
            if single_count == 4 :
                finger_detected[now_finger] = 1    

#---------------------------------------------------------------------------------
#手指判斷
def finger_identify(pos_y4,pos_x4,pos_y3,pos_x3,avg_x,avg_y,hand_landmarks,image_height,image_width,finger_detected,FINGER) :       
    detected_length=100      #判定手指與重心點長度(會影響檢測距離)
    if (((pos_y4 < pos_y3) & (pos_y4 < int(image_height * hand_landmarks.landmark[0].y))) or  #手朝上
        ((pos_y4 > pos_y3) & (pos_y4 > int(image_height * hand_landmarks.landmark[0].y))) or  #手朝下
        ((pos_x4 < pos_x3) & (pos_x4 < int (image_width * hand_landmarks.landmark[0].x))) or  #手朝左 
        ((pos_x4 > pos_x3) & (pos_x4 > int (image_width * hand_landmarks.landmark[0].x)))) :  #手朝右
        if abs(pos_x4-avg_x) >= detected_length or abs(pos_y4-avg_y) >= detected_length :
            finger_detected[FINGER] = 1

#---------------------------------------------------------------------------------
#描繪ROI框與擷取圖片
def catching_start(image,image_proto,start_count,start_x,start_y,finger_detected,ROI_x,ROI_y) :

    if start_count < 20 :   #抓取間隔(影響觸發擷取框的秒數)
        cv2.rectangle(image,(ROI_x,ROI_y-100),(ROI_x+100,ROI_y),(0,0,255),3)
        #print(start_count,finger_detected)
        #起始手勢
        if finger_detected [2] & finger_detected[3] & ~finger_detected[1] & ~finger_detected[4] & ~finger_detected[5] :
            start_x,start_y = ROI_x,ROI_y-100
            start_count = start_count + 1
        else :
            start_count = 0
    else :
        cv2.putText(image,"Catching Start",(0,55),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
        cv2.rectangle(image,(start_x,start_y),(ROI_x,ROI_y),(0,0,255),3)
        #停止手勢
        if finger_detected[2] & ~finger_detected[3] :     
            start_count = 0
            #裁切圖片
            if (ROI_x < start_x) & (ROI_y < start_y)   :  #擷取左上框
                crop_image=image_proto[ROI_y:start_y,ROI_x:start_x]
            elif (ROI_x > start_x) & (ROI_y < start_y) :  #擷取右上框
                crop_image=image_proto[ROI_y:start_y,start_x:ROI_x]
            elif (ROI_x < start_x) & (ROI_y > start_y) :  #擷取左下框
                crop_image=image_proto[start_y:ROI_y,ROI_x:start_x]
            elif (ROI_x > start_x) & (ROI_y > start_y) :  #擷取右下框
                crop_image=image_proto[start_y:ROI_y,start_x:ROI_x]
            #裁切圖片<0的檢測判斷
            crop_image_height,crop_image_weight,_=crop_image.shape
            if(crop_image_height & crop_image_weight) :
                crop_image=cv2.flip(crop_image, 1)
                #crop_image=cv2.resize(crop_image,dsize=(1024,768),interpolation=cv2.INTER_CUBIC)
                cv2.imshow("cropped image",crop_image)
                cv2.imwrite("output.png",crop_image)
                
                # 圖片二值化
                test_img=cv2.cvtColor(crop_image,cv2.COLOR_RGB2GRAY)
                cv2.imshow("blur img",test_img)
                #test_img=cv2.GaussianBlur(test_img, (5,5), 0)
                test_img=cv2.medianBlur(test_img, 3)
                test_img=cv2.adaptiveThreshold(test_img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3)
                cv2.imshow("test_img",test_img)
                cv2.imwrite("output_blurred.png",test_img)
                

                #OCR文字辨識
                OCR_text=OCR_func()
                print(OCR_text)
                zh_tw_trans=google_translate(OCR_text)
                print(zh_tw_trans)

    return start_count,start_x,start_y
#---------------------------------------------------------------------------------
#OCR文字辨識
def OCR_func():
    #Tesserat辨識文字
    img = Image.open("output.png")
    #text=pytesseract.image_to_string(img, lang="eng",config='--psm 6')
    text=pytesseract.image_to_string(img, lang="chi_tra",config='--psm 6')
    return text

#Google文字翻譯
def google_translate(text):
    google_translator=Translator()
    res=google_translator.translate(text,dest='zh-tw').text
    #res=google_translator.translate(text,dest='en').text
    return res



#---------------------------------------------------------------------------------
#主程式
def main(image,image_proto,hand_landmarks,start_count,start_x,start_y) :
    image_height, image_width, _ = image.shape  #圖形長寬
    ROI_x,ROI_y=0,0                             #ROI初始化
    finger_detected=[0 for x in range(0,6)]     #1:大拇指,2:食指,3:中指,4:無名指,5:小拇指

    #計算中心點座標
    avg_x,avg_y,center = avg_point(image,hand_landmarks,image_height,image_width)

    #判斷單指重覆點
    single_detected(image,hand_landmarks,finger_detected,image_height,image_width)
    
    for FINGER in range(1,6) :
        #指頭節點
        pos_x4=int(image_width * (hand_landmarks.landmark[4*FINGER].x))
        pos_y4=int(image_height * (hand_landmarks.landmark[4*FINGER].y))
        #次指頭節點
        pos_x3=int(image_width * (hand_landmarks.landmark[4*FINGER-1].x))
        pos_y3=int(image_height * (hand_landmarks.landmark[4*FINGER-1].y))

        #辨識手指
        finger_identify(pos_y4,pos_x4,pos_y3,pos_x3,avg_x,avg_y,hand_landmarks,image_height,image_width,finger_detected,FINGER)

        #紀錄ROI(食指)位置
        ROI_x,ROI_y=(int(image_width*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x)),
                    int(image_height*(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y)))
        
    #開始圖片抓取與剪裁
    start_count,start_x,start_y=catching_start(image,image_proto,start_count,start_x,start_y,finger_detected,ROI_x,ROI_y)
    
        
    return center,ROI_x,ROI_y,start_count,start_x,start_y
    
   