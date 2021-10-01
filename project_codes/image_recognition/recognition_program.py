from state import State
from position import Position
import HAND
import USER
import cv2
import mediapipe as mp
import numpy as np

from handedness_detector import get_handedness

from finger_trigger import if_only_index_finger, if_indexNmiddle_finger
from text_recognition import text_recognition
from video_source_selector import VideoSource


class STATE:
    WaitingSignal = State("Waiting signal to crop")
    StartCropping = State("Start cropping")
    DoingCropping = State("Doing cropping")
    FinishCropping = State("Finish cropping")
    GetText = State("To get text")

    GetTextFailed = State("Getting text failed")

    Error = State("Error")
    FinishRecognition = State("Done with Recognition")


class STATE_CROPPING:
    Start = State("Start cropping")
    Doing = State("Doing cropping")
    End = State("Finish cropping")


class STATE_LIGHTNESS:
    Fine = State("Fine")
    TooBright = State("too bright")
    TooDim = State("too dim")


class ROI_frame:
    start = Position("start")
    end = Position("end")


# mediapipe solution group
mp_hands = mp.solutions.hands

NUM_POINT_HAND = 21
NUM_DIMENSION = 3


class edit_img:
    def put_text(img, str_show_text):
        cv2.putText(img, str_show_text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)

    def draw_point(img, position):
        point = (position.x, position.y)
        point_radius = 3
        point_color = (0, 0, 255)
        point_thickness = -1  # whole point fill in point_color

        cv2.circle(
            img, point, radius=point_radius, color=point_color, thickness=point_thickness)

    def draw_frame(img, position_start, position_end):
        p1 = (position_start.x, position_start.y)
        p2 = (position_end.x, position_end.y)
        frame_color = (255, 105, 65)
        frame_thickness = 2

        cv2.rectangle(img, p1, p2, color=frame_color,
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

        self._tolerance = 0
        self._flag_change_state = False

        self.Position_initial = Position("Position Initial")
        self.index_finger_point = Position("Position of Index_Finger")
        self.Position_final = Position("Position Final")

        self._input_img = []
        self.output_img = []
        self.crop_img = []

        self.hand_results = []

        self.list_point_hand = [1] * NUM_POINT_HAND * NUM_DIMENSION
        self.handedness = HAND.NO
        self._only_index_finger = False
        self._only_indexNmiddle_finger = False

        self.state_lightness = []
        self.average_gray_value = 0

        self.text = ""

    def _debug_print_statement(self):
        """
        debug
        """
        if self._tolerance != 0 and self._tolerance < self.MAX_TOLERANCE:
            print(self._tolerance, end=",")
        elif self._tolerance == self.MAX_TOLERANCE:
            print(self._tolerance)

        if self.now_state != self.last_state or self.next_state != self.last_state:
            self.last_state = self.now_state
            print(self.now_state, ", ", self.next_state)
            print("only_index_finger: ", self._only_index_finger, ", only_indexNmiddle_finger: ",
                  self._only_indexNmiddle_finger, ", flag_change_state: ", self._flag_change_state)
            print(self.Position_initial)
            print(self.Position_final)
        else:
            pass

    def _update_whole_hand_point(self):
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

    def _update_index_finger_point(self):
        """
        update self.index_finger_point

        [need to update self.list_point_hand first]
        """
        self.index_finger_point.x = int(self.list_point_hand[NUM_DIMENSION*8]*float(
            self._input_img.shape[1]))
        self.index_finger_point.y = int(self.list_point_hand[NUM_DIMENSION*8+1]*float(
            self._input_img.shape[0]))

    def _update_hand_point(self):
        """
        update: handedness, list_point_hand, index_finger_point
        """
        self.handedness = get_handedness(self.hand_results.multi_handedness)
        self._update_whole_hand_point()
        self._update_index_finger_point()

    def _update_state_lightness(self):
        """
        update average_gray_value and state_lightness
        """
        self.average_gray_value = np.mean(self._input_img)

        if self.average_gray_value > self.MAX_AVERAGE_GRAY_VALUE:
            self.state_lightness = STATE_LIGHTNESS.TooBright
        elif self.average_gray_value < self.MIN_AVERAGE_GRAY_VALUE:
            self.state_lightness = STATE_LIGHTNESS.TooDim
        else:
            self.state_lightness = STATE_LIGHTNESS.Fine

    def _show_output_img_original(self):
        self.output_img = self._input_img
        self.output_img = cv2.flip(self.output_img, 1)
        cv2.imshow('Output Image', self.output_img)

    def _show_output_img_edited(self):
        self.output_img = self._input_img
        edit_img.draw_frame(
            self.output_img, self.Position_initial, self.Position_final)
        edit_img.draw_point(self.output_img, self.Position_final)
        self.output_img = cv2.flip(self.output_img, 1)
        if self.state_lightness != STATE_LIGHTNESS.Fine:
            edit_img.put_text(self.output_img, str(self.state_lightness))
        cv2.imshow('Output Image', self.output_img)

    def _do_WaitingSignal(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self._only_index_finger = if_only_index_finger(
                self.list_point_hand)

        self._show_output_img_original()

    def _do_StartCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self.Position_initial.x, self.Position_initial.y = self.index_finger_point()
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self._show_output_img_original()

    def _do_DoingCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self._only_index_finger = if_only_index_finger(
                self.list_point_hand)
            self._only_indexNmiddle_finger = if_indexNmiddle_finger(
                self.list_point_hand)
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self._update_state_lightness()
        self._show_output_img_edited()

    def _do_FinishCropping(self):
        """
        output: crop_img
        """
        if self.Position_initial.x > self.Position_final.x:
            self.Position_initial.x, self.Position_final.x = self.Position_final.x, self.Position_initial.x
        if (self.Position_initial.y > self.Position_final.y):
            self.Position_initial.y, self.Position_final.y = self.Position_final.y, self.Position_initial.y

        self.output_img = cv2.flip(self.output_img, 1)
        self.crop_img = self.output_img[self.Position_initial.y: self.Position_final.y,
                                        self.Position_initial.x: self.Position_final.x]
        self.crop_img = cv2.flip(self.crop_img, 1)

        self.Position_initial.x = self.Position_initial.y = self.Position_final.x = self.Position_final.y = 0
        self._only_index_finger = self._only_indexNmiddle_finger = False

    def _do(self):
        """
        do what should do with state
        1. edit output_img
        2. update event
        """
        if self.now_state == STATE.WaitingSignal:
            self._do_WaitingSignal()
        elif self.now_state == STATE.StartCropping:
            self._do_StartCropping()
        elif self.now_state == STATE.DoingCropping:
            self._do_DoingCropping()
        elif self.now_state == STATE.FinishCropping:
            self._do_FinishCropping()
        elif self.now_state == STATE.GetText:
            self.text = text_recognition(self.crop_img)
        elif self.now_state == STATE.GetTextFailed:
            pass
        elif self.now_state == STATE.FinishRecognition:
            pass
        elif self.now_state == STATE.Error:
            assert 0, "error state, last state: %r" % (self.last_state)
            pass
        else:  # unknown state
            assert 0, "unknown state, last state: %r" % (self.last_state)
            pass

    def _check_tolerance(self):
        if self.next_state == self.now_state:
            self._tolerance = 0
            self._flag_change_state = False
        else:
            if self._tolerance > self.MAX_TOLERANCE:
                self._tolerance = 0
                self._flag_change_state = True
            else:
                self._tolerance = self._tolerance + 1
                self._flag_change_state = False

    def _update_flag_if_can_change_state(self):
        """"
        update_flag_if_can_change_state
        """
        if self.now_state == STATE.WaitingSignal:
            self._check_tolerance()
        elif self.now_state == STATE.StartCropping:
            self._check_tolerance()
        elif self.now_state == STATE.DoingCropping:
            if (self.Position_initial.x != self.Position_final.x) and (self.Position_initial.y != self.Position_final.y):
                self._check_tolerance()
            else:
                self._flag_change_state = False

        elif self.now_state == STATE.FinishCropping:
            self._flag_change_state = True
        elif self.now_state == STATE.GetText:
            self._flag_change_state = True
        elif self.now_state == STATE.GetTextFailed:
            self._flag_change_state = True
        elif self.now_state == STATE.FinishRecognition:
            self._flag_change_state = True
        elif self.now_state == STATE.Error:
            self._flag_change_state = True
        else:  # unknown state
            self._flag_change_state = False

    def _update_next_state(self):
        """
        change_next_state by singal(s) with each state
        """
        if self.now_state == STATE.WaitingSignal:
            if self.handedness == USER.HANDEDNESS and self._only_index_finger:
                self.next_state = STATE.StartCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.StartCropping:
            self.next_state = STATE.DoingCropping
        elif self.now_state == STATE.DoingCropping:
            if self.handedness == USER.HANDEDNESS and self._only_indexNmiddle_finger:
                self.next_state = STATE.FinishCropping
            elif self.handedness == USER.HANDEDNESS and self._only_index_finger:
                self.next_state = STATE.DoingCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.FinishCropping:
            if self.state_lightness == STATE_LIGHTNESS.Fine:
                self.next_state = STATE.GetText
            else:
                self.next_state = STATE.DoingCropping

        elif self.now_state == STATE.GetText:
            self.next_state = STATE.FinishRecognition
        elif self.now_state == STATE.GetTextFailed:
            self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.FinishRecognition:
            self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.Error:
            self.next_state = self.STATE_INITIAL
        else:  # unknown state
            self.next_state = self.STATE_INITIAL

    def _change_state_if_needed(self):
        self._update_next_state()
        self._update_flag_if_can_change_state()

        if self._flag_change_state:
            self.now_state = self.next_state

    def _process_state_mechine(self):
        """
        1. do what should do
        2. change state if needed
        """
        self._do()
        self._change_state_if_needed()

    def run_program(self):
        """
        1. get input_img, hand_results
        2. do what should do during change state, until finish doing recognition
        """

        with mp_hands.Hands(
                static_image_mode=False,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.7,
                max_num_hands=1)as hands:

            cap = VideoSource(1)

            while cap.isOpened():
                success, self._input_img = cap.read()
                resized_rate = 1
                dsize = (int(
                    self._input_img.shape[1]*resized_rate), int(self._input_img.shape[0]*resized_rate))
                self._input_img = cv2.resize(self._input_img, dsize)

                if not success:
                    #print("Ignoring empty camera frame.")
                    continue
                else:
                    self._input_img = cv2.flip(self._input_img, 1)
                    img = self._input_img
                    img = cv2.cvtColor(self._input_img, cv2.COLOR_BGR2RGB)
                    img.flags.writeable = False
                    self.hand_results = hands.process(img)

                    self._process_state_mechine()

                    # debug
                    self._debug_print_statement()

                    if(self.now_state == STATE.FinishRecognition):
                        # pass
                        print(self.text)
                        # cv2.waitKey(1000)
                        # break

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
        Recognition.run_program()
        return Recognition.text

    except:
        assert 0, "main_recognition failed"
        pass


if __name__ == "__main__":
    text = main_recognition()
    print("result: [\n%r\n]" % text)
