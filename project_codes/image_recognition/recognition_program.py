from .position import Position
from .state import State

import cv2
import mediapipe as mp
import numpy as np


from .finger_trigger import if_only_index_finger, if_indexNmiddle_finger
from .text_recognition import text_recognition
from .video_source_selector import VideoSource

state_message = {
    "WaitingSignal": "等待截圖",
    "StartCropping": "開始截圖",
    "DoingCropping": "正在截圖",
    "FinishCropping": "完成截圖",
    "GetText": "正在辨識文字",
    "FinishRecognition": "完成辨識"
}


class STATE:
    WaitingSignal = State(state_message["WaitingSignal"])
    StartCropping = State(state_message["StartCropping"])
    DoingCropping = State(state_message["DoingCropping"])
    FinishCropping = State(state_message["FinishCropping"])
    GetText = State(state_message["GetText"])

    GetTextFailed = State("Getting text failed")

    Error = State("Error")
    FinishRecognition = State(state_message["FinishRecognition"])


class STATE_CROPPING:
    Start = State("Start cropping")
    Doing = State("Doing cropping")
    End = State("Finish cropping")


class STATE_LIGHTNESS:
    Fine = State("Fine")
    TooBright = State("too bright")
    TooDim = State("too dim")


class STATE_HANDEDNESS:
    No = State("No Hand")
    Not = State("Not user handedness")
    Is = State("Is user handedness")


class ROI_frame:
    start = Position("start")
    end = Position("end")


# mediapipe solution group
mp_hands = mp.solutions.hands

NUM_POINT_HAND = 21
NUM_DIMENSION = 3

HD_SIZE = 720

red_color = (0, 0, 255)

max_store_index_finger_point_number = 5


def update_stored_point(stored_point_list, new_point, pointer):
    stored_point_list[pointer].x, stored_point_list[pointer].y = new_point()

    return stored_point_list


def get_stabilized_finger(stored_point_list, stored_point_length=max_store_index_finger_point_number):
    """
    stored_point_list must be in class Position
    """
    total_sum_x = 0
    total_sum_y = 0

    for index in range(stored_point_length):
        total_sum_x = total_sum_x + stored_point_list[index].x
        total_sum_y = total_sum_y + stored_point_list[index].y

    stabilized_finger_point_x = int(total_sum_x/stored_point_length)
    stabilized_finger_point_y = int(total_sum_y/stored_point_length)
    return [stabilized_finger_point_x, stabilized_finger_point_y]


def get_dsize(height, weight, max_size=HD_SIZE):
    if height > HD_SIZE:
        resized_rate = HD_SIZE/height
        dsize = (int(height*resized_rate), int(weight*resized_rate))
    else:
        dsize = (int(height), int(weight))

    return dsize


def update_show_size(height, weight, cut_percentage=0.1):
    """
    get_show_size for make user seems don't whole hand on the camera
    """
    show_weight_i = int(weight * cut_percentage/2)  # compiler friendly
    show_height_i = int(height * cut_percentage)
    show_height_f = int(height)
    show_weight_f = int(weight - show_weight_i)

    return [show_height_i, show_height_f, show_weight_i, show_weight_f]


class edit_img:
    def put_text(img, str_show_text, text_color=(0, 255, 255)):
        cv2.putText(img, str_show_text, (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 1, cv2.LINE_AA)

    def draw_point(img, position, point_color=red_color, point_radius=3):
        point = (position.x, position.y)
        point_thickness = -1  # whole point fill in point_color

        cv2.circle(
            img, point, radius=point_radius, color=point_color, thickness=point_thickness)

    def draw_frame(img, position_start, position_end, frame_color=red_color, frame_thickness=1):
        p1 = (position_start.x, position_start.y)
        p2 = (position_end.x, position_end.y)

        cv2.rectangle(img, p1, p2, color=frame_color,
                      thickness=frame_thickness)


class RecognitionProgram:
    STATE_INITIAL = STATE.WaitingSignal
    MAX_TOLERANCE = 3
    MAX_AVERAGE_GRAY_VALUE = 180
    MIN_AVERAGE_GRAY_VALUE = 100
    MIN_CROP_SCALE = 10
    MIN_DETECTION_CONFIDENCE = 0.7
    MIN_TRACKING_CONFIDENCE = 0.7
    MAX_OVERTIME_ROI = 20

    def __init__(self):
        """
        initialization of recognition_program
        """
        self.now_state = self.STATE_INITIAL
        self.last_state = None
        self.next_state = self.STATE_INITIAL

        self._selected_camera = 0
        self.cap = VideoSource(self._selected_camera)

        self._tolerance = 0
        self._flag_change_state = False

        self.Position_initial = Position("Position Initial")
        self.index_finger_point = Position("Position of Index_Finger")
        self.Position_final = Position("Position Final")

        self._counter_overtime_ROI = 0
        self._flag_overtime_ROI = False

        self._stored_point_list = []
        for i in range(max_store_index_finger_point_number):
            new_position = Position(str(i))
            new_position.x, new_position.y = self.Position_final()
            self._stored_point_list.append(new_position)

        self._new_point = Position("new_point")
        self._new_point_pointer = 0

        self._input_img = cv2.imread("./project_codes/init_img.png")
        self.output_img = self._input_img
        self.crop_img = self._input_img

        self._temp_output_img = None
        self._temp_crop_img = None
        self._flag_success_cropping = False

        self.hand_results = None

        self.list_point_hand = [1] * NUM_POINT_HAND * NUM_DIMENSION
        # self.handedness = HAND.NO
        self._only_index_finger = False
        self._only_indexNmiddle_finger = False

        self.state_lightness = None
        self.average_gray_value = (
            self.MIN_AVERAGE_GRAY_VALUE + self.MAX_AVERAGE_GRAY_VALUE)/2

        self.text = ""

        self._flag_can_get_text = False

    def has_recognited_text(self):
        return self._flag_can_get_text

    def ack_had_got_recognited_text(self):
        self._flag_can_get_text = False

    def _debug_print_statement(self):
        """
        debug
        """
        if self._tolerance != 0 and self._tolerance < self.MAX_TOLERANCE:
            print(self._tolerance, end=",")
        elif self._tolerance == self.MAX_TOLERANCE:
            print(self._tolerance)

        if self.now_state != self.last_state or self.next_state != self.last_state:
            print(self.last_state, ", ", self.now_state, ", ", self.next_state)
            self.last_state = self.now_state
            # print(f"only_index_finger: {self._only_index_finger}, only_indexNmiddle_finger:{self._only_indexNmiddle_finger}, flag_change_state: {self._flag_change_state}")
            # print(self.Position_initial)
            # print(self.Position_final)
            print(self.text)
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

    def _update_stored_pointer(self):
        self._new_point.x = int(self.list_point_hand[NUM_DIMENSION*8]*float(
            self._input_img.shape[1]))
        self._new_point.y = int(self.list_point_hand[NUM_DIMENSION*8+1]*float(
            self._input_img.shape[0]))

        self._stored_point_list = update_stored_point(
            self._stored_point_list, self._new_point, self._new_point_pointer)

        self._new_point_pointer = self._new_point_pointer + 1
        if self._new_point_pointer == max_store_index_finger_point_number:
            self._new_point_pointer = 0

    def _update_index_finger_point(self):
        """
        update self.index_finger_point

        [need to update self.list_point_hand first]
        """
        self.index_finger_point.x, self.index_finger_point.y = get_stabilized_finger(
            self._stored_point_list)

    def _update_hand_point(self):
        """
        update: handedness, list_point_hand, index_finger_point
        """
        # self.handedness = get_handedness(self.hand_results.multi_handedness)
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

    def _update_output_img(self):
        # self.output_img = self._input_img[self._show_size[2]:self._show_size[3],
        #                                   self._show_size[1]:self._show_size[0]]
        self.output_img = self._input_img
        #self.output_img = cv2.flip(self.output_img, 1)
        #cv2.imshow("input", self._input_img)
        #cv2.imshow("show", self.output_img)

    def _update_output_img_edited(self):
        # self.output_img = self._input_img[self._show_size[2]:self._show_size[3],
        #                                  self._show_size[0]:self._show_size[1]].copy()
        self._temp_output_img = self._input_img.copy()
        edit_img.draw_frame(
            self._temp_output_img, self.Position_initial, self.Position_final)
        edit_img.draw_point(self._temp_output_img, self.Position_final)
        self.output_img = self._temp_output_img
        # self.output_img = cv2.flip(self.output_img, 1)

    def _do_WaitingSignal(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self._only_index_finger = if_only_index_finger(
                self.list_point_hand)

        self._update_output_img()

    def _do_StartCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self.Position_initial.x, self.Position_initial.y = self.index_finger_point()
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self._update_output_img()

    def _update_flag_overtime_ROI(self):
        if self._stored_point_list[0].x == self._stored_point_list[self._new_point_pointer].x:
            if self._counter_overtime_ROI < self.MAX_OVERTIME_ROI:
                self._counter_overtime_ROI = self._counter_overtime_ROI + 1
                self._flag_overtime_ROI = False
            else:
                self._counter_overtime_ROI = 0
                self._only_index_finger = False
                self._flag_overtime_ROI = True
        else:
            self._counter_overtime_ROI = 0
            self._flag_overtime_ROI = False

    def _do_DoingCropping(self):
        if self.hand_results.multi_hand_landmarks:
            self._update_hand_point()
            self._only_index_finger = if_only_index_finger(
                self.list_point_hand)
            self._only_indexNmiddle_finger = if_indexNmiddle_finger(
                self.list_point_hand)
            self.Position_final.x, self.Position_final.y = self.index_finger_point()

        self._update_flag_overtime_ROI()
        self._update_output_img_edited()

    def _do_FinishCropping(self):
        """
        output: crop_img
        """
        try:
            if self.Position_initial.x > self.Position_final.x:
                self.Position_initial.x, self.Position_final.x = self.Position_final.x, self.Position_initial.x
            if (self.Position_initial.y > self.Position_final.y):
                self.Position_initial.y, self.Position_final.y = self.Position_final.y, self.Position_initial.y

            self._temp_crop_img = self._input_img.copy()
            self.crop_img = self._temp_crop_img[self.Position_initial.y: self.Position_final.y,
                                                self.Position_initial.x: self.Position_final.x]

            self.Position_initial.x = self.Position_initial.y = self.Position_final.x = self.Position_final.y = 0
            self._only_index_finger = self._only_indexNmiddle_finger = False
            if self.crop_img.shape[1] != 0:
                self._counter_overtime_ROI = 0
                self._flag_success_cropping = True
            else:
                self._flag_success_cropping = False
        except:
            self._flag_success_cropping = False

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
            # print('from HAND: Recognition text : ', self.text, time.time_ns())
            self._flag_can_get_text = True
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
            if self._flag_overtime_ROI == False:
                diff_x = self.Position_initial.x - self.Position_final.x
                diff_y = self.Position_initial.y - self.Position_final.y
                # if self.MIN_CROP_SCALE < (diff_x + diff_y):
                if 0 != diff_x + diff_y:  # means Position_initial != Position_final
                    self._check_tolerance()
                else:
                    self._flag_change_state = False
            else:
                self._flag_change_state = True

        elif self.now_state == STATE.FinishCropping:
            if self._flag_success_cropping:
                self._flag_change_state = True
            else:
                self._flag_change_state = False
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
            # if self.handedness == USER.HANDEDNESS and self._only_index_finger:
            if self._only_index_finger:
                self.next_state = STATE.StartCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.StartCropping:
            if self.Position_initial.x != 0:
                self.next_state = STATE.DoingCropping
            else:
                self.next_state = STATE.StartCropping
        elif self.now_state == STATE.DoingCropping:
            # if self.handedness == USER.HANDEDNESS and self._only_indexNmiddle_finger:
            if self._flag_overtime_ROI == False:
                if self._only_indexNmiddle_finger:
                    self.next_state = STATE.FinishCropping
                # elif self.handedness == USER.HANDEDNESS and self._only_index_finger:
                elif self._only_index_finger:
                    self.next_state = STATE.DoingCropping
                else:
                    self.next_state = STATE.WaitingSignal
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.FinishCropping:
            self.next_state = STATE.GetText
            # if self.state_lightness == STATE_LIGHTNESS.Fine:
            #    self.next_state = STATE.GetText
            # else:
            #    self.next_state = STATE.DoingCropping

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

    def get_recognited_text(self):
        return self.text

    def run_program(self):
        """
        selected_camare:
            0 - local front camare
            1 or else - other local camare, or local webcamare
            url - url of IpWebcam

        run_program to update input_img, hand_results, text
        """
        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=4,
                model_complexity=0,
                min_detection_confidence=self.MIN_DETECTION_CONFIDENCE,
                min_tracking_confidence=self.MIN_TRACKING_CONFIDENCE)as hands:
            for _ in iter(int, 1):
                success, self._input_img = self.cap.read()

                if success:
                    dsize = get_dsize(
                        self._input_img.shape[1], self._input_img.shape[0], max_size=HD_SIZE)
                    self._show_size = update_show_size(
                        self._input_img.shape[0], self._input_img.shape[1])
                    print(self._input_img.shape[0], self._input_img.shape[1])
                    print(self._show_size[0], self._show_size[1],
                          self._show_size[2], self._show_size[3])
                    _ = text_recognition(self.crop_img)
                    print(_)
                    break

            while self.cap.isOpened():
                success, self._input_img = self.cap.read()

                # speed up mediapipe process, img of too large size will be slow
                # self._input_img = cv2.resize(self._input_img, dsize)

                if not success:
                    # print("Ignoring empty camera frame.")
                    continue
                else:
                    # self._input_img = cv2.flip(self._input_img, 1)
                    img = self._input_img
                    img = cv2.cvtColor(self._input_img, cv2.COLOR_BGR2RGB)
                    img.flags.writeable = False
                    self.hand_results = hands.process(img)

                    self._update_state_lightness()
                    self._process_state_mechine()
                    self._update_stored_pointer()
                    self._debug_print_statement()

                    if cv2.waitKey(1) & 0xFF == 27:
                        """
                        wait 1ms, and & 0xFF
                        for complement to the key we want (ascii 27 = esc)
                        """
                        break
            self.cap.release()
