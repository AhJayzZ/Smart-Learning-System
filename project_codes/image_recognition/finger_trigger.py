class triggers:
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


def finger_trigger(list):
    trigger = triggers(list)

    thumb = trigger.thumb()
    index_finger = trigger.index_finger()
    middle_finger = trigger.middle_finger()
    ring_finger = trigger.ring_finger()
    pinky = trigger.pinky()

    finger_trigger_list = [thumb,
                           index_finger,
                           middle_finger,
                           ring_finger,
                           pinky]

    return finger_trigger_list
