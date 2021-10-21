from get_word_info import get_word_info
from translate_fromENtoCN import translator

#input: text_str
#output: translated_text_str or text_info_dict


def check_if_one_word(text_str):
    check_list = " ,!%~.;\"'1234567890#$&-+=[{"

    for char in text_str:
        if char in check_list:
            return 0

    return 1


def selector_TranslateOrWord(text_str, src="en", dest="zh-tw"):
    if text_str == "":
        # do something if you want
        pass
    else:
        if check_if_one_word(text_str):
            return get_word_info(text_str)
        else:
            return translator(text_str, src="en", dest="zh-tw")
