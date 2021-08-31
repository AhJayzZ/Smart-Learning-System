# 輸入一段英文文字，翻譯成繁體中文
# input: WordToTranslate_str
# output: WordTranslated_str
# usage: translator(WordToTranslate_str)

def translator(WordToTranslate_str):
    from googletrans import Translator
    translator = Translator()
    translation = translator.translate(
        WordToTranslate_str, src='en', dest='zh-tw').text
    return translation
