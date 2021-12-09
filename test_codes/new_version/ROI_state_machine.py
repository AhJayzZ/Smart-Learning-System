
class State:
    """
        class State

        example:
            State_WaitingSignal = State("Waiting signal to crop")
            print(State_WaitingSignal)
            # output: Waiting signal to crop
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class STATE:
    WaitingSignal = State("Waiting signal to crop")
    StartCropping = State("Start cropping")
    DoingCropping = State("Doing cropping")
    FinishCropping = State("Finish cropping")

    Error = State("Error")  # unknown state will be turned to this state


class ROI_state_machine:
    STATE_INITIAL = STATE.WaitingSignal
    MAX_TOLERANCE = 5

    def __init__(self):
        self.now_state = self.STATE_INITIAL
        self.last_state = None  # debug
        self.next_state = self.STATE_INITIAL

        self._flag_change_state = False

        self._tolerance = 0
        self._flag_change_state = False

        self._ROI_frame = [(0, 0), (0, 0)]

    def _check_tolerance(self):
        """
        make not change state immediately
        """
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

    def _update_next_state(self, if_only_index_finger, if_only_index_and_middle_finger):
        """
            change_next_state by singal(s) with each state
            signal: if_only_index_finger, if_only_index_and_middle_finger
        """
        if self.now_state == STATE.WaitingSignal:
            # if self.handedness == USER.HANDEDNESS and self._only_index_finger:
            if if_only_index_finger:
                self.next_state = STATE.StartCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.StartCropping:
            self.next_state = STATE.DoingCropping
        elif self.now_state == STATE.DoingCropping:
            # if self.handedness == USER.HANDEDNESS and self._only_indexNmiddle_finger:
            if if_only_index_and_middle_finger:
                self.next_state = STATE.FinishCropping
            # elif self.handedness == USER.HANDEDNESS and self._only_index_finger:
            elif if_only_index_finger:
                self.next_state = STATE.DoingCropping
            else:
                self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.FinishCropping:
            self.next_state = STATE.WaitingSignal
        elif self.now_state == STATE.Error:
            # can do logging here
            self.next_state = self.STATE_INITIAL
        else:  # unknown state
            self.next_state = STATE.Error

    def _update_flag_change_state(self):
        """"
        update_flag_if_can_change_state
        """
        if self.now_state == STATE.WaitingSignal:
            self._check_tolerance()
        elif self.now_state == STATE.StartCropping:
            self._check_tolerance()
        elif self.now_state == STATE.DoingCropping:
            if (self._ROI_frame[0][0] != self._ROI_frame[1][0]) and (self._ROI_frame[0][1] != self._ROI_frame[1][1]):
                self._check_tolerance()
            else:
                self._flag_change_state = False
        elif self.now_state == STATE.FinishCropping:
            self._flag_change_state = True

        elif self.now_state == STATE.Error:
            self._flag_change_state = True
        else:  # unknown state
            self._flag_change_state = False

    def _update_ROI_frame(self, index_finger_point):
        if self.now_state == STATE.WaitingSignal:
            pass
        elif self.now_state == STATE.StartCropping:
            self._ROI_frame[0] = index_finger_point
        elif self.now_state == STATE.DoingCropping:
            self._ROI_frame[1] = index_finger_point
        elif self.now_state == STATE.FinishCropping:
            self._ROI_frame[1] = index_finger_point

            if self._ROI_frame[0][0] > self._ROI_frame[1][0]:
                self._ROI_frame[0][0], self._ROI_frame[1][0] = self._ROI_frame[1][0], self._ROI_frame[0][0]
            if (self._ROI_frame[0][1] > self._ROI_frame[1][1]):
                self._ROI_frame[0][1], self._ROI_frame[1][1] = self._ROI_frame[1][1], self._ROI_frame[0][1]
        elif self.now_state == STATE.Error:
            #assert 0, "error state, last state: %r" % (self.last_state)
            pass
        else:  # unknown state
            #assert 0, "unknown state, last state: %r" % (self.last_state)
            pass

    def get_ROI(self, if_only_index_finger, if_only_index_and_middle_finger, index_finger_point):
        """
            get hand recognition
        """
        self.last_state = self.now_state
        self._update_next_state(if_only_index_finger,
                                if_only_index_and_middle_finger)
        self._update_flag_change_state()
        if self._flag_change_state:
            self.now_state = self.next_state
        self._update_ROI_frame(index_finger_point)

        if self.now_state != self.last_state:
            print(self._ROI_frame, self.now_state)
        return self._ROI_frame
