
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


class state_machine:
    STATE_INITIAL = STATE.WaitingSignal
    MAX_TOLERANCE = 5

    def __init__(self):
        self.now_state = self.STATE_INITIAL
        #self.last_state = None
        self.next_state = self.STATE_INITIAL

        self._tolerance = 0
        self._flag_change_state = False

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

    def get_now_state(self):
        return self.now_state

    def _update_next_state(self, if_only_index_finger, if_only_indexNmiddle_finger):
        """
            change_next_state by singal(s) with each state
            signal: 
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
            if if_only_indexNmiddle_finger:
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
