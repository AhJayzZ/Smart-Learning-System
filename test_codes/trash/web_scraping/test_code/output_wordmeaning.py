from googletrans import Translator

text = "apple"

translator = Translator()
translation = translator.translate(text, src='en', dest='zh-tw')
print(translation.origin, ' -> ', translation.text)