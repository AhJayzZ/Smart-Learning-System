"""
handednedd_detector: function about handedness 
"""
import HAND


def get_handedness(results):
    """
        Args: 
            kind of json(still not sure about) by results.multi_handedness, as results

        Raises: -

        Returns: handedness in HAND [LEFT = 0,RIGHT = 1,NO = -1]
    """
    results = str(results)

    if "Left" in results:
        return HAND.LEFT
    elif "Right" in results:
        return HAND.RIGHT
    else:
        return HAND.NO
