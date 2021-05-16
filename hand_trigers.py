import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
list= [0]*63

class trigers:
    def __init__(self,list):
        self.list = list
        self.a = ((self.list[15]-self.list[0])**2+(self.list[16]-self.list[1])**2)**0.5   # 點5到點0距離 
        self.b = ((self.list[27]-self.list[0])**2+(self.list[28]-self.list[1])**2)**0.5   # 點9到點0距離
        self.c = ((self.list[39]-self.list[0])**2+(self.list[40]-self.list[1])**2)**0.5   # 點13到點0距離
        self.d = ((self.list[51]-self.list[0])**2+(self.list[52]-self.list[1])**2)**0.5   # 點17到點0距離
        self.e = (((self.list[51]-self.list[15])**2+(self.list[52]-self.list[16])**2)**0.5)*1.2   # 點5到點17距離

    # 點與點之間的距離
    def distance(self,x1,y1,x2,y2):
        dis=0
        dis= (((x1-x2)**2+(y1-y2)**2)**0.5)/ max(self.a,self.b,self.c,self.d,self.e) 
        return dis

    # 計算各點手部landmark與wirst的距離和
    def distance_sum(self):
        sum=0
        for i in range(1,21):
            sum+= self.distance(self.list[3*i],self.list[3*i+1],self.list[0],self.list[1]) 
        return sum

    # 計算所有點的中心
    def center_all(self):
        sum_x=0
        sum_y=0
        for i in range(21):
            sum_x+= self.list[3*i]
            sum_y+= self.list[3*i+1]
        return sum_x/21, sum_y/21
    # 斜率
    def slope(self,x1,y1,x2,y2):
        return (y2-y1)/(x2-x1)

    # 若大拇指伸直:True; 否則: False
    def thumb (self):
        # 離散程度
        thumb_dis_a= self.distance(self.list[12],self.list[13],self.list[6],self.list[7])
        thumb_dis_b= self.distance(self.list[9],self.list[10],self.list[6],self.list[7])

        # 拇指各點到線(兩端點連成的直線)的距離和
        m= self.slope(self.list[0],self.list[1],self.list[12],self.list[13])    # 直線斜率
        b= (self.list[1])- m*(self.list[0])   # 直線參數: y=slope*x+b => b= y-slope*x
        line= lambda x,y: abs(m*x-y+b)      # 直線方程
        point_to_line=0     #   拇指各點到線的和
        for point in range(1,4):
            point_to_line+= (line(self.list[3*point],self.list[3*point+1])/(m**2+1)**0.5)/ max(self.a,self.b,self.c,self.d,self.e)  # 公式


        if (thumb_dis_a+thumb_dis_b) > 0.67 and (point_to_line<0.4):
            return True
        else:
            return False

    # 若食指伸直:True; 否則: False
    def index_finger (self):
        index_finger_dis_a= self.distance(self.list[24],self.list[25],self.list[15],self.list[16])
        index_finger_dis_b= self.distance(self.list[21],self.list[22],self.list[15],self.list[16])
        index_finger_dis_c= self.distance(self.list[18],self.list[19],self.list[15],self.list[16])

        # 食指各點到線(兩端點連成的直線)的距離和
        m= self.slope(self.list[3*5],self.list[3*5+1],self.list[3*8],self.list[3*8+1])    # 直線斜率
        b= (self.list[3*5+1])- m*(self.list[3*5])   # 直線參數: y=slope*x+b => b= y-slope*x
        line= lambda x,y: abs(m*x-y+b)      # 直線方程
        point_to_line=0     #   拇指各點到線的和
        for point in range(6,8): # 點
            point_to_line+= (line(self.list[3*point],self.list[3*point+1])/(m**2+1)**0.5)/ max(self.a,self.b,self.c,self.d,self.e)  # 公式

        if (index_finger_dis_a+index_finger_dis_b+index_finger_dis_c)>1 and (index_finger_dis_a>index_finger_dis_b) and (index_finger_dis_b>index_finger_dis_c) and (point_to_line<0.12):
            return True
        else:
            return False
    # 若中指伸直:True; 否則: False
    def middle_finger (self):
        middle_finger_dis_a= self.distance(self.list[36],self.list[37],self.list[27],self.list[28])
        middle_finger_dis_b= self.distance(self.list[33],self.list[34],self.list[27],self.list[28])
        middle_finger_dis_c= self.distance(self.list[30],self.list[31],self.list[27],self.list[28])

        # 中指各點到線(兩端點連成的直線)的距離和
        m= self.slope(self.list[3*9],self.list[3*9+1],self.list[3*12],self.list[3*12+1])    # 直線斜率
        b= (self.list[3*9+1])- m*(self.list[3*9])   # 直線參數: y=slope*x+b => b= y-slope*x
        line= lambda x,y: abs(m*x-y+b)      # 直線方程
        point_to_line=0     #   拇指各點到線的和
        for point in range(10,12): # 點
            point_to_line+= (line(self.list[3*point],self.list[3*point+1])/(m**2+1)**0.5)/ max(self.a,self.b,self.c,self.d,self.e)  # 公式

        if (middle_finger_dis_a+middle_finger_dis_b+middle_finger_dis_c)>1.1 and (middle_finger_dis_a>middle_finger_dis_b) and (middle_finger_dis_b>middle_finger_dis_c) and (point_to_line<0.12):
            return True
        else:
            return False
    # 若無名指伸直:True; 否則: False
    def ring_finger (self):
        ring_finger_dis_a= self.distance(self.list[48],self.list[49],self.list[39],self.list[40])
        ring_finger_dis_b= self.distance(self.list[45],self.list[46],self.list[39],self.list[40])
        ring_finger_dis_c= self.distance(self.list[42],self.list[43],self.list[39],self.list[40])

        # 無名指各點到線(兩端點連成的直線)的距離和
        m= self.slope(self.list[3*13],self.list[3*13+1],self.list[3*16],self.list[3*16+1])    # 直線斜率
        b= (self.list[3*13+1])- m*(self.list[3*13])   # 直線參數: y=slope*x+b => b= y-slope*x
        line= lambda x,y: abs(m*x-y+b)      # 直線方程
        point_to_line=0     #   拇指各點到線的和
        for point in range(14,16): # 點
            point_to_line+= (line(self.list[3*point],self.list[3*point+1])/(m**2+1)**0.5)/ max(self.a,self.b,self.c,self.d,self.e)  # 公式

        if (ring_finger_dis_a+ring_finger_dis_b+ring_finger_dis_c) > 1.15 and (ring_finger_dis_a>ring_finger_dis_b) and (ring_finger_dis_b>ring_finger_dis_c) and(point_to_line<0.12) :
            return True
        else:
            return False

    # 若小拇指伸直:True; 否則: False
    def pinky (self):
        pinky_dis_a= self.distance(self.list[60],self.list[61],self.list[51],self.list[52])
        pinky_dis_b= self.distance(self.list[57],self.list[58],self.list[51],self.list[52])
        pinky_dis_c= self.distance(self.list[54],self.list[55],self.list[51],self.list[52])

        # 小拇指各點到線(兩端點連成的直線)的距離和
        m= self.slope(self.list[3*17],self.list[3*17+1],self.list[3*20],self.list[3*20+1])    # 直線斜率
        b= (self.list[3*17+1])- m*(self.list[3*17])   # 直線參數: y=slope*x+b => b= y-slope*x
        line= lambda x,y: abs(m*x-y+b)      # 直線方程
        point_to_line=0     #   拇指各點到線的和
        for point in range(18,20): # 點
            point_to_line+= (line(self.list[3*point],self.list[3*point+1])/(m**2+1)**0.5)/ max(self.a,self.b,self.c,self.d,self.e)  # 公式


        if (pinky_dis_a+pinky_dis_b+pinky_dis_c) > 0.9 and (pinky_dis_a>pinky_dis_b)and(pinky_dis_b>pinky_dis_c) and (point_to_line<0.1) :
            return True
        else:
            return False

    # 顯示數字
    def some_pose(self):
        if not self.index_finger() and not self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "ZERO", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "ONE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and not self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "TWO", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and not self.thumb() and self.ring_finger() and not self.pinky():
            cv2.putText(image, "THREE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and not self.thumb() and  self.ring_finger() and  self.pinky():
            cv2.putText(image, "FOUR", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and  self.thumb() and  self.ring_finger() and  self.pinky():
            cv2.putText(image, "FIVE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if not self.index_finger() and not self.middle_finger() and  self.thumb() and not self.ring_finger() and  self.pinky():
            cv2.putText(image, "SIX", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and  self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "SEVEN", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and  self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "EIGHT", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and  self.middle_finger() and  self.thumb() and  self.ring_finger() and not self.pinky():
            cv2.putText(image, "NINE", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if self.index_finger() and not self.middle_finger() and  self.thumb() and not self.ring_finger() and  self.pinky():
            cv2.putText(image, "ROCK", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)
        if not self.index_finger() and not self.middle_finger() and  self.thumb() and not self.ring_finger() and not self.pinky():
            cv2.putText(image, "Good Game", (10, 40), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 255), 2, cv2.LINE_AA)


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
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
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # cv2.COLOR_BGR2GRAY 
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        # print(hand_landmarks.landmark[8]) # 顯示位置 mp_hands.HandLandmark.INDEX_FINGER_TIP
        # 用一個長度為63的矩陣，儲存21個手的特徵點(x,y,z)
        # 排序方式為[ 0的x,y,z; 1的x,y,z...] 
        for i in range(21):             
            list[3*i]=float(hand_landmarks.landmark[i].x)
            list[3*i+1]=float(hand_landmarks.landmark[i].y)
            list[3*i+2]=float(hand_landmarks.landmark[i].z)

        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    triger = trigers(list)
    triger.some_pose()


    cv2.imshow('MediaPipe Hands', image)  
    if cv2.waitKey(1) & 0xFF == 27:
      break
cap.release()