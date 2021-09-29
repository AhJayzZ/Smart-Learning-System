import cv2


def VideoSource(selected_camare):
    """
    selected_camare:
        0 - local front camare
        1 or else - other local camare, or local webcamare
        url - url of IpWebcam
    """
    if int(selected_camare):
        if selected_camare == 0:
            cap = cv2.VideoCapture(selected_camare)
        else:
            # avoid VideoCapture() taking so long, but maybe got potential problem here
            # https://www.notion.so/CV2-Webcam-10-3cd585408e9141ca9254d84df9f6b66c
            cap = cv2.VideoCapture(selected_camare, cv2.CAP_DSHOW)

        return cap
    else:
        """url of IpWebcam"""
        cap = cv2.VideoCapture(selected_camare)

        return cap
