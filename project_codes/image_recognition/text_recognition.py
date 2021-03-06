import pytesseract
from .cropped_img_handler import cropped_img_handler
from .text_correction import get_corrected_text

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def text_recognition(image_for_get_text):
    try:
        new_image_for_get_text = cropped_img_handler(image_for_get_text)
        # white text with black backgroud, could not be recognited correctly
        # text = pytesseract.image_to_string(new_image_for_get_text, lang='eng')

        # test codes: if get img to pytesseract directly
        text = pytesseract.image_to_string(image_for_get_text, lang='eng')

        # print(text)
        text = get_corrected_text(text)
        # print(text)
        return text
    except:
        #assert 0, "error with {text_recognition.__name__}"
        print("empty frame")
        pass
