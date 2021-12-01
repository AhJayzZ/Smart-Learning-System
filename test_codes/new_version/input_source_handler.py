from absl.flags import Flag
import cv2
from matplotlib.pyplot import show

HD_SIZE = 720
REFRESH_TIME = 5  # ms


def get_dsize(height, weight, limit_size=HD_SIZE):
    """
        get_dsize with resized_rate, which depended on max_size
    """
    if height > limit_size:
        resized_rate = limit_size/height
        dsize = (int(height*resized_rate), int(weight*resized_rate))
    else:
        dsize = (int(height), int(weight))

    return dsize


def VideoSource(selected_camare=0):
    """
        selected_camare:
            0 - local front camare
            1 or else - other local camare, or local webcamare
            url - url of IpWebcam
    """
    if isinstance(selected_camare, int):
        if selected_camare == 0:
            cap = cv2.VideoCapture(selected_camare)
        else:
            # avoid VideoCapture() taking so long, but maybe got potential problem here
            cap = cv2.VideoCapture(selected_camare, cv2.CAP_DSHOW)

        return cap
    else:
        """url of IpWebcam"""
        cap = cv2.VideoCapture(selected_camare)

        return cap


class input_source_handler():
    """
        method:
            1. keep_get_input_img(dsize=HD_size): start refresh frame in each 5 ms
            2. change_video_source(video_source)
            3. change_frameMode(frameMode)
            4. get_frame()
            5. get_flag_enable_to_get_frame()
    """

    def __init__(self, video_source):
        self._input_img_source = video_source
        self._cap = VideoSource(self._input_img_source)

        self._flag_change_video_source = False  # for inside using
        self._flag_enable_to_get_frame = False  # for outside using
        self._resize_size = None
        self._frame = []  # use get_frame for outside using

        self._frame_mode = 2  # defualt, don't do change

    def change_video_source(self, video_source):
        """
            function: change video source while camera is on
            input: video_source, can be given by
                0(default local camare),
                1 or other integer more then one(other local webcamare), or 
                url(url of IpWebcam)
        """
        self._flag_enable_to_get_frame = False
        self._flag_change_video_source = True
        self._input_img_source = video_source

    def change_frameMode(self, frameMode):
        """
            input: frameMode, can be given by
                2(defualt, don't do change)
                1(Horizontal flip),
                0(Vertical flip), or
                -1(Horizontal & Vertical flip)
        """
        self._frame_mode = frameMode

    def get_frame(self):
        """
            output for hand_recognition
        """
        return self._frame

    def get_flag_enable_to_get_frame(self):
        """
            output for hand_recognition
        """
        return self._flag_enable_to_get_frame

    def keep_refresh_frame(self, dsize=HD_SIZE):
        """
            for main program

            input: dsize(optional)
            function: start refresh frame in each 1 ms
                - resized frame to reduce recognition time
        """
        for _ in iter(int, 1):  # for-loop in Python is faster than while-loop
            success, ori_frame = self._cap.read()

            if success:
                self._resize_size = get_dsize(
                    ori_frame.shape[1], ori_frame.shape[0], limit_size=dsize)
                break
            else:
                # print("capture failed")
                pass

        while self._cap.isOpened():
            if not self._flag_change_video_source:
                success, ori_frame = self._cap.read()
                resize_frame = cv2.resize(ori_frame, self._resize_size)

                if success:
                    if self._frame_mode == 2:
                        self._frame = resize_frame
                    else:
                        self._frame = cv2.flip(resize_frame, self._frame_mode)
                    self._flag_enable_to_get_frame = True
                else:
                    #print("Ignoring empty camera frame.")
                    self._flag_enable_to_get_frame = False
            else:
                self._cap.release()
                self._cap = VideoSource(self._input_img_source)
                self._flag_change_video_source = False

            cv2.waitKey(REFRESH_TIME)
