import requests
from bs4 import BeautifulSoup
from googletrans import Translator

# 輸入單詞，取得單詞相關資料
# input: word_str
# output: wordInfo_dict，
#   including [
#              'word', #format in str
#              'eng_pr', #format in str
#              'ame_pr', #format in str
#              'tenses', #format in str
#              'defination' #format in str, had translated from 'zh-cn'to 'zh-tw'
#              'def_eng' #format in dict
#             ]
#   all in str
'''
    usage e.g.:
    word_str = "food"
    wordInfo_dict = get_word_info(word_str)
    print(wordInfo_dict)
'''

dict_replace_str = {
    "1.": ".1.",
    "2.": ".2.",
    "3.": ".3.",
    "4.": ".4.",
    "5.": ".5.",
    "6.": ".6.",
    "7.": ".7.",
    "8.": ".8.",
    "9.": ".9.",
    ".": ". ",
    ". . ": ". ",
    ". ,": ".,",
    "  ": ""
}


class DictRstParser:
    def soup_context(self, word_str):
        try:
            URL = f"https://www.bing.com/dict/search?q={word_str}"
            HEADERS = {'cookie': '_EDGE_S=F&mkt=zh-cn'}
            webpage = requests.get(URL, headers=HEADERS)
            soup = BeautifulSoup(webpage.text, 'html.parser')
            return soup
        except:
            print("get soup_context failed")
            return None

    def get_content(self, from_obj, selector_str):
        rst = from_obj.select(selector_str)
        if len(rst) == 0:
            return None
        elif len(rst) == 1:
            return rst[0].get_text().replace("\xa0", " ").strip()
        else:
            return '\n'.join([e.get_text() for e in rst])

    def get_url_mp3(self):
        try:
            ame_url_mp3_raw = self.soup.select(
                'body > div.contentPadding > div > div > div.lf_area > div.qdef > div.hd_area > div.hd_tf_lh > div > div:nth-child(2) > a')
            [throw_head, ame_url_mp3] = str(ame_url_mp3_raw[0]).split(
                "Click(this,\'", maxsplit=1)
            [ame_url_mp3, throw_tail] = ame_url_mp3.split(
                "','", maxsplit=1)

            eng_url_mp3_raw = self.soup.select(
                'body > div.contentPadding > div > div > div.lf_area > div.qdef > div.hd_area > div.hd_tf_lh > div > div:nth-child(4) > a')
            [throw_head, eng_url_mp3] = str(eng_url_mp3_raw[0]).split(
                "Click(this,\'", maxsplit=1)
            [eng_url_mp3, throw_tail] = eng_url_mp3.split(
                "','", maxsplit=1)

            return [ame_url_mp3, eng_url_mp3]
        except:
            print("get url_mp3 failed")
            pass

    def get_def_eng(self):
        def_eng_raw = self.soup.find_all(id='homoid')[0]
        list_raw = []
        for row in def_eng_raw.find_all('tr'):
            list_raw.append(row.text)

        for index in range(len(list_raw)):
            for key, value in dict_replace_str.items():
                list_raw[index] = list_raw[index].replace(key, value)

        return list_raw

    def __init__(self, word_str):
        try:
            self.soup = self.soup_context(word_str)
            self.word_info_selector_dict = {
                'word': 'div#headword',
                'eng_pr': 'div.hd_pr',
                'ame_pr': 'div.hd_prUS',
                # 'synonym': 'div.wd_div',
                'tenses': 'div.hd_div1',
                'defination': 'div.qdef > ul > li',
            }

            self.word_info_dict = {}
            translator = Translator()
            self.related_divs = self.soup.select('div.lf_area > div')
            for k, v in self.word_info_selector_dict.items():
                self.word_info_dict[k] = self.get_content(
                    self.related_divs[0], v)
                if(self.word_info_dict[k] != None):
                    translation = translator.translate(
                        self.word_info_dict[k], src='zh-cn', dest='zh-tw')
                    self.word_info_dict[k] = translation.text

            # [self.word_info_dict['ame_pr_url'],
            #    self.word_info_dict['eng_pr_url']] = self.get_url_mp3()

            self.word_info_dict['defination'] = self.word_info_dict['defination'].replace(
                "網絡", "網絡：", 1)
            self.word_info_dict['defination'] = self.word_info_dict['defination'].replace(
                "\n", " | ")
            self.word_info_dict['def_eng'] = self.get_def_eng()

        except:
            print("Try another word")
            self.word_info_dict = None
            pass


'''
    self.word_info_dict['sentences'] = self.get_content(
        self.related_divs[1], 'div#sentenceSeg')'''


def get_word_info(word_str):
    parser = DictRstParser(word_str)
    wordInfo_dict = parser.word_info_dict
    return wordInfo_dict


if __name__ == "__main__":
    word_str = "feeling"
    wordInfo_dict = get_word_info(word_str)
    print(wordInfo_dict)
