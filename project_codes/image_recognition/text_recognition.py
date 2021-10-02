import pytesseract
from .crop_img_handler import crop_img_handler
from .text_correction import get_corrected_text

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def text_recognition(image_for_get_text):
    try:
        image_for_get_text = crop_img_handler(image_for_get_text)

        text = pytesseract.image_to_string(image_for_get_text, lang='eng')
        text = get_corrected_text(text)
        return text
    except:
        assert 0, "error with {text_recognition.__name__}"
        pass
