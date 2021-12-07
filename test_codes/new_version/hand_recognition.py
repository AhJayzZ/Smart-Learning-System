import cv2
import mediapipe as mp
from finger_trigger import if_only_index_finger, if_indexNmiddle_finger
from input_source_handler import input_source_handler
from ROI_state_machine import ROI_state_machine

mp_hands = mp.solutions.hands

NUM_POINT_HAND = 21
NUM_DIMENSION = 3

REFRESH_TIME = 5  # ms

user_video_source = 1
camera = input_source_handler(user_video_source)


def draw_point(img, position, point_color=(0, 0, 255), point_radius=3):
    point = position
    point_thickness = -1  # whole point fill in point_color

    cv2.circle(
        img, point, radius=point_radius, color=point_color, thickness=point_thickness)


def draw_frame(img, position_start, position_end, frame_color=(255, 105, 65), frame_thickness=2):
    p1 = position_start
    p2 = position_end

    cv2.rectangle(img, p1, p2, color=frame_color,
                  thickness=frame_thickness)


class hand_recognition:
    """
        method:
            1. run(input_source_handler)
            4. get_recognited_frame()
            5. get_index_finger_point()
    """

    def __init__(self):
        self._results = []
        self._frame = []
        self._list_point_hand = [float(0)] * NUM_POINT_HAND * NUM_DIMENSION
        self._index_finger_point = (0, 0)

        self._only_index_finger = False
        self._only_index_and_middle_finger = False

        self._ROI_frame = [(0, 0), (0, 0)]

    def _refresh_hand_point_and_event(self):
        """
        update _list_point_hand, _only_index_finger, _only_index_and_middle_finger
        """
        if self._results.multi_hand_landmarks:
            # turn mediapipe hand_landmarks format to list, which order to x,y,z in row
            for hand_landmarks in self._results.multi_hand_landmarks:
                i = 0
                for i in range(NUM_POINT_HAND):
                    self._list_point_hand[NUM_DIMENSION *
                                          i] = float(hand_landmarks.landmark[i].x)
                    self._list_point_hand[NUM_DIMENSION * i +
                                          1] = float(hand_landmarks.landmark[i].y)
                    self._list_point_hand[NUM_DIMENSION * i +
                                          2] = float(hand_landmarks.landmark[i].z)

                    i = i + 1

            self._only_index_finger = if_only_index_finger(
                self._list_point_hand)
            self._only_index_and_middle_finger = if_indexNmiddle_finger(
                self._list_point_hand)

            index_finger_point_x = int(self._list_point_hand[NUM_DIMENSION*8]*float(
                self._frame.shape[1]))
            index_finger_point_y = int(self._list_point_hand[NUM_DIMENSION*8+1]*float(
                self._frame.shape[0]))
            self._index_finger_point = (
                index_finger_point_x, index_finger_point_y)
        else:
            # default value
            self._list_point_hand = [float(0)] * NUM_POINT_HAND * NUM_DIMENSION
            self._only_index_finger = False
            self._only_index_and_middle_finger = False
            self._index_finger_point = (0, 0)

    def get_recognited_frame(self):
        """
            for text recognition & output frame handler
        """
        return self._frame

    def get_ROI(self):
        """
            for output frame handler
        """
        return self._ROI_frame

    def _if_only_index_finger(self):
        """
            for state_mechine
        """
        return self._only_index_finger

    def _if_only_index_and_middle_finger(self):
        """
            for state_mechine
        """
        return self._only_index_and_middle_finger

    def _get_index_finger_point(self):
        """
            for state_mechine
        """
        return self._index_finger_point

    def run(self,
            user_min_detection_confidence=0.7,
            user_min_tracking_confidence=0.7):  # hand_recognition.run(i_img.get_frame())
        """
            for main program: start run to update input_img, hand_results
        """
        ROI = ROI_state_machine()
        input_source = input_source_handler()

        with mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=4,
                model_complexity=0,
                min_detection_confidence=user_min_detection_confidence,
                min_tracking_confidence=user_min_tracking_confidence
        )as hands:
            for _ in iter(int, 1):  # for-loop in Python is faster than while-loop
                # bad design here: we need to know input_source_handler had those method
                if input_source.get_flag_enable_to_get_frame():  # enable to get frame
                    self._frame = input_source.get_frame()

                    img_for_recognition = cv2.cvtColor(
                        self._frame, cv2.COLOR_BGR2RGB)
                    img_for_recognition.flags.writeable = False
                    self._results = hands.process(img_for_recognition)

                    self._refresh_hand_point_and_event()
                    self._ROI_frame = ROI.get_ROI(
                        self._if_only_index_finger(),
                        self._if_only_index_and_middle_finger(),
                        self._get_index_finger_point()
                    )

                    cv2.imshow("output", self._frame)

                else:  # loss frame
                    pass

                cv2.waitKey(REFRESH_TIME)


if __name__ == "__main__":
    recognition = hand_recognition()
    recognition.run()
