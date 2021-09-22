import cv2
import mediapipe as mp
import numpy as np

from handedness_detector import get_handedness

from finger_trigger import if_only_index_finger, if_indexNmiddle_finger

from text_recognition import text_recognition

import USER
import HAND

# class
from position import Position
from state import State

# state group


class STATE:
    WaitingSignal = State("Waiting signal to crop")
    StartCropping = State("Start cropping")
    DoingCropping = State("Doing cropping")
    FinishCropping = State("Finish cropping")
    GetText = State("To get text")

    GetTextFailed = State("Getting text failed")
    WarningTooBright = State("Warning: too bright")
    WarningTooDim = State("Warning: too dim")

    Error = State("Error")
    FinishRecognition = State("Done with Recognition")


# mediapipe solution group
mp_hands = mp.solutions.hands

# never used
#mp_drawing = mp.solutions.drawing_utils
#mp_drawing_styles = mp.solutions.drawing_styles

NUM_POINT_HAND = 21
NUM_DIMENSION = 3


class edit_image:
    def put_text(image, str_show_text):
        cv2.putText(image, str_show_text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

    def draw_point(image, position):
        point = (position.x, position.y)
        point_radius = 3
        point_color = (0, 0, 255)
        point_thickness = -1  # whole point fill in point_color

        cv2.circle(
            image, point, radius=point_radius, color=point_color, thickness=point_thickness)

    def draw_frame(image, position_start, position_end):
        p1 = (position_start.x, position_start.y)
        p2 = (position_end.x, position_end.y)
        frame_color = (255, 105, 65)
        frame_thickness = 2

        cv2.rectangle(image, p1, p2, color=frame_color,
                      thickness=frame_thickness)


class recognition_program:
    STATE_INITIAL = STATE.WaitingSignal
    MAX_TOLERANCE = 5
    MAX_AVERAGE_GRAY_VALUE = 180
    MIN_AVERAGE_GRAY_VALUE = 100

    def __init__(self):
        """
        initialization of recognition_program
        """
        self.now_state = self.STATE_INITIAL
        self.last_state = []
        self.next_state = self.STATE_INITIAL

        self.tolerance = 0
        self.flag_change_state = False

        self.Position_initial = Position("Position Initial")
        self.index_finger_point = Position("Position of Index_Finger")
        self.Position_final = Position("Position Final")

        self.input_image = []
        self.output_image = []
        self.crop_image = []

        self.hand_results = []

        self.list_point_hand = [1] * NUM_POINT_HAND * NUM_DIMENSION
        self.handedness = HAND.NO
        self.only_index_finger = False
        self.only_indexNmiddle_finger = False

        self.average_gray_value = 0

        self.text = ""

    def print_debug_statement(self):
        """
        debug
        """
        if self.tolerance != 0 and self.tolerance < self.MAX_TOLERANCE:
            print(self.tolerance, end=",")
        elif self.tolerance == self.MAX_TOLERANCE:
            print(self.tolerance)

        if self.now_state != self.last_state or self.next_state != self.last_state:
            self.last_state = self.now_state
            print(self.now_state, ", ", self.next_state, ", ",
                  self.only_index_finger, self.only_indexNmiddle_finger, self.flag_change_state)
            print(self.Position_initial)
            print(self.Position_final)
        else:
            pass

    def update_whole_hand_point(self):
        """
        update self.list_point_hand
        """
        for hand_landmarks in self.hand_results.multi_hand_landmarks:
            i = 0
            for i in range(NUM_POINT_HAND):
                self.list_point_hand[NUM_DIMENSION *
                                     i] = float(hand_landmarks.landmark[i].x)
                self.list_point_hand[NUM_DIMENSION * i +
                                     1] = float(hand_landmarks.landmark[i].y)
                self.list_point_hand[NUM_DIMENSION * i +
                                     2] = float(hand_landmarks.landmark[i].z)

                i = i + 1

    def update_index_finger_point(self):
        """
        update self.index_finger_point

        [need to update self.list_point_hand first]
        """
        self.index_finger_point.x = int(self.list_point_hand[NUM_DIMENSION*8]*float(
            self.input_image.shape[1]))
        self.index_finger_point.y = int(self.list_point_hand[NUM_DIMENSION*8+1]*float(
            self.input_image.shape[0]))

    def update_hand_point(self):
        """
        update: handedness, list_point_hand, index_finger_point
        """
        self.handedness = get_handedness(self.hand_results.multi_handedness)
        self.update_whole_hand_point()
        self.update_index_finger_point()

    def show_output_image_original(self):
        self.output_image = cv2.flip(self.input_image, 1)
        cv2.imshow('Output Image', self.output_image)

    def show_output_image_edited(self):
        self.output_image = cv2.flip(self.input_image, 1)
        edit_image.draw_frame(
            self.output_image, self.Position_initial, self.Position_final)
        edit_image.draw_point(self.output_image, self.Position_final)
        #edit_image.put_text(self.output_image, str(self.now_state))
        cv2.imshow('Output Image', self.output_image)

    def do_WaitingSignal(self):
        if self.hand_results.multi_hand_landmarks:
            self.update_hand_point()
            self.only_index_finger = if_only_index_finger(
                self.list_point_hand)

        self.show_output_image_original()

    def do_StartCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self.update_hand_point()
            self.Position_initial.x, self.Position_initial.y = self.index_finger_point()
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self.show_output_image_original()

    def do_DoingCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self.update_hand_point()
            self.only_index_finger = if_only_index_finger(
                self.list_point_hand)
            self.only_indexNmiddle_finger = if_indexNmiddle_finger(
                self.list_point_hand)
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self.show_output_image_edited()

    def do_FinishCropping(self):
        if self.Position_initial.x > self.Position_final.x:
            self.Position_initial.x, self.Position_final.x = self.Position_final.x, self.Position_initial.x
        if (self.Position_initial.y > self.Position_final.y):
            self.Position_initial.y, self.Position_final.y = self.Position_final.y, self.Position_initial.y

        self.crop_image = self.output_image[self.Position_initial.y: self.Position_final.y,
                                            self.Position_initial.x: self.Position_final.x]

        self.average_gray_value = np.mean(self.crop_image)  # 計算圖片平均灰度
        cv2.destroyWindow('Output Image')
        cv2.imshow('crop_image', self.crop_image)

    def do(self):
        """
        do what should do with state
        1. edit output_image
        2. update event
        """
        if self.now_state == STATE.WaitingSignal:
            self.do_WaitingSignal()
        elif self.now_state == STATE.StartCropping:
            self.do_StartCropping()
        elif self.now_state == STATE.DoingCropping:
            self.do_DoingCropping()
        elif self.now_state == STATE.FinishCropping:
            self.do_FinishCropping()
        elif self.now_state == STATE.GetText:
            self.text = text_recognition(self.crop_image)
        elif self.now_state == STATE.GetTextFailed:
            pass
        elif self.now_state == STATE.WarningTooBright:
            pass
        elif self.now_state == STATE.WarningTooDim:
            pass
        elif self.now_state == STATE.FinishRecognition:
            pass
        elif self.now_state == STATE.Error:
            assert 0, "error state, last state: %r" % (self.last_state)
            pass
        else:  # unknown state
            assert 0, "unknown state, last state: %r" % (self.last_state)
            pass

    def check_tolerance(self):
        if self.next_state == self.now_state:
            self.tolerance = 0
            self.flag_change_state = False
        else:
            if self.tolerance > self.MAX_TOLERANCE:
                self.tolerance = 0
                self.flag_change_state = True
            else:
                self.tolerance = self.tolerance + 1
                self.flag_change_state = False

    def update_flag_if_can_change_state(self):
        """"
        update_flag_if_can_change_state
        """
        if self.now_state == STATE.WaitingSignal:
            self.check_tolerance()
        elif self.now_state == STATE.StartCropping:
            self.flag_change_state = True
        elif self.now_state == STATE.DoingCropping:
            if (self.Position_initial.x != self.Position_final.x) and (self.Position_initial.y != self.Position_final.y):
                self.check_tolerance()
            else:
                self.flag_change_state = False

        elif self.now_state == STATE.FinishCropping:
            self.flag_change_state = True
        elif self.now_state == STATE.GetText:
            self.flag_change_state = True
        elif self.now_state == STATE.GetTextFailed:
            self.flag_change_state = True
        elif self.now_state == STATE.WarningTooBright:
            self.flag_change_state = True
        elif self.now_state == STATE.WarningTooDim:
            self.flag_change_state = True
        elif self.now_state == STATE.FinishRecognition:
            self.flag_change_state = False
        elif self.now_state == STATE.Error:
            self.flag_change_state = True
        else:  # unknown state
            self.flag_change_state = False

    def update_next_state(self):
        """
        change_next_state by singal(s) with each state
        """
        if self.now_state == STATE.WaitingSignal:
            if self.handedness == USER.HANDEDNESS and self.only_index_finger:
                self.next_state = STATE.StartCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.StartCropping:
            self.next_state = STATE.DoingCropping
        elif self.now_state == STATE.DoingCropping:
            if self.handedness == USER.HANDEDNESS and self.only_indexNmiddle_finger:
                self.next_state = STATE.FinishCropping
            elif self.handedness == USER.HANDEDNESS and self.only_index_finger:
                self.next_state = STATE.DoingCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.FinishCropping:
            if self.average_gray_value > self.MAX_AVERAGE_GRAY_VALUE:
                self.next_state = STATE.WarningTooDim
            elif self.average_gray_value < self.MIN_AVERAGE_GRAY_VALUE:
                self.next_state = STATE.WarningTooBright
            else:
                self.next_state = STATE.GetText

        elif self.now_state == STATE.GetText:
            self.next_state = STATE.FinishRecognition
        elif self.now_state == STATE.GetTextFailed:
            self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.WarningTooDim:
            self.next_state = STATE.DoingCropping
        elif self.now_state == STATE.WarningTooBright:
            self.next_state = STATE.DoingCropping
        elif self.now_state == STATE.FinishRecognition:
            self.next_state = STATE.FinishRecognition
        elif self.now_state == STATE.Error:
            self.next_state = self.STATE_INITIAL
        else:  # unknown state
            self.next_state = self.STATE_INITIAL

    def change_state_if_needed(self):
        self.update_next_state()
        self.update_flag_if_can_change_state()

        if self.flag_change_state:
            self.now_state = self.next_state

    def process(self):
        """
        1. do what should do
        2. change state if needed
        """
        self.do()
        self.change_state_if_needed()

    def run(self):
        """
        1. get input_image, hand_results
        2. do what should do during change state, until finish doing recognition
        """

        with mp_hands.Hands(
                static_image_mode=False,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7,
                max_num_hands=1)as hands:

            cap = cv2.VideoCapture(USER.DEFAULT_CAMERA)
            while cap.isOpened():
                success, self.input_image = cap.read()

                if not success:
                    assert 0, "Ignoring empty camera frame."
                    continue
                else:
                    image = cv2.cvtColor(
                        cv2.flip(self.input_image, 1), cv2.COLOR_BGR2RGB)
                    self.input_image.flags.writeable = False
                    self.hand_results = hands.process(image)

                    self.process()

                    # debug
                    self.print_debug_statement()

                    if(self.now_state == STATE.FinishRecognition):
                        break

                    if cv2.waitKey(1) & 0xFF == 27:
                        """
                        wait 1ms, and & 0xFF
                        for complement to the key we want (ascii 27 = esc)
                        """
                        break

            cap.release()


def main_recognition():
    try:
        """from timeit import Timer
        t = Timer("Recognition = recognition_program()",
                  "from main_recognition import recognition_program")
        print(t.timeit())
        # 20210915 last test: 1.5569038999999982
        """
        Recognition = recognition_program()
        Recognition.run()
        return Recognition.text

    except:
        assert 0, "main_recognition failed"
        pass


if __name__ == "__main__":
    text = main_recognition()
    print("result: [\n%r\n]" % text)
