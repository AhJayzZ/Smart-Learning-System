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
