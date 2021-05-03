from cv2 import cv2
import mediapipe as mp
import PoseTable as  pose_table

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

#開始製作ROI框
start_count = 0
start_x,start_y = 0,0

# For webcam input:
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5,max_num_hands=1)
#鏡頭選擇與解析度設定(最高為1280*720,預設480*640)
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
while cap.isOpened():
  success, image = cap.read()
  if not success:
    print("Ignoring empty camera frame.")
    # If loading a video, use 'break' instead of 'continue'.
    continue
  
 
  
  # Flip the image horizontally for a later selfie-view display,Convertx the BGR image to RGB.
  image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
  # To improve performance, optionally mark the image as not writeable to pass by reference.
  image.flags.writeable = False
  results = hands.process(image)
  

  # Hold prototype image for cropping image
  image_proto=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

  # Draw the hand annotations on the image.
  image.flags.writeable = False
  image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

  annotated_image = image.copy()

  if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
      mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    #連結所有手部節點  
    mp_drawing.draw_landmarks(annotated_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    #進行手勢的辨別(採x,y座標相減)
    for hand_landmarks in results.multi_hand_landmarks:
      center,ROI_x,ROI_y,start_count,start_x,start_y=pose_table.main(image,image_proto,hand_landmarks,start_count,start_x,start_y)
    


    #打印出中心點位置與食指中心點位置
    cv2.putText(image,"Center Point:" + str(center) ,(0,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
    cv2.putText(image,"ROI Center Point:" + str((ROI_x,ROI_y)) ,(0,35),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1,cv2.LINE_AA)
   
  #調整視窗大小與輸出影像
  cv2.imshow('MediaPipe Hands', image)

  if cv2.waitKey(5) & 0xFF == 27 :
    break
hands.close()
cap.release()