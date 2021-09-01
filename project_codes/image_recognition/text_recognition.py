import pytesseract


def text_recognition(image_for_get_text):
    try:
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        text = pytesseract.image_to_string(image_for_get_text, lang='eng')
        return text
    except:
        print("error with {text_recognition.__name__}")
        pass
