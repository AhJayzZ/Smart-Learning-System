from cv2 import imshow
import pytesseract
from .cropped_img_handler import cropped_img_handler
from .text_correction import get_corrected_text

pytesseract.pytesseract.tesseract_cmd = "project_codes\\image_recognition\\pytesseract.exe"


def text_recognition(image_for_get_text):
    try:
        image_for_get_text = cropped_img_handler(image_for_get_text)

        text = pytesseract.image_to_string(image_for_get_text, lang='eng')
        # print(text)
        text = get_corrected_text(text)
        # print(text)
        return text
    except:
        assert 0, "error with {text_recognition.__name__}"
        #print("empty frame")
        pass
