import pytesseract
from PIL import Image
image = Image.open('ch.png')
text = pytesseract.image_to_string(image, lang='chi_tra')
print(text)