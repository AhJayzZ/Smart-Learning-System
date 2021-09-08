"""
state of recognition
"""

WAIT_HANDEDNESS = 0
WAIT_ONLY_INDEX_FINGER = 1
START_CROP = 2
CROPPING = 3
END_CROP = 4
GET_WORDS = 5


def print_state(state):
    """

    """
    state_list = {
        "WAIT_HANDEDNESS",
        "WAIT_ONLY_INDEX_FINGER",
        "START_CROP",
        "CROPPING",
        "END_CROP",
        "GET_WORDS"
    }
    print(state_list[state])
