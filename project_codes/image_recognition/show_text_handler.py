import cv2
import STATE


def show_text_handler(image, state_recognition):
    if(state_recognition == STATE.CROPPING):
        str_show_text = "cropping"
    else:
        str_show_text = "do nothing"

    cv2.putText(image, str_show_text, (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
