import requests
from bs4 import BeautifulSoup

# test word
text = "fish"
text1 = "fire"


def function_failed_statement():
    import traceback
    print(traceback.extract_stack(None, 2)[0][2], "failed")


def get_soup(text):
    try:
        home_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        headers = {'User-Agent': user_agent}
        word_url = home_url + str(text)
        res = requests.get(word_url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(res.text, 'html.parser')
        return soup
    except:
        function_failed_statement()
        pass


def get_meaning_chinese(soup):
    try:
        meaning_chinese_raw = soup.find(
            "meta", {"itemprop": "headline"})["content"]
        [throwHead, meaning_chinese] = meaning_chinese_raw.split(": ", 1)
        [meaning_chinese, throwTail] = meaning_chinese.split(". ", 1)
        meaning_chinese = meaning_chinese.split(", ")
        return meaning_chinese
    except:
        function_failed_statement()
        pass


def get_meaning_PartOfSpeech_eg(soup):
    try:
        meaning_chinese_raw = soup.find_all(
            "span", {"class": "pos dpos"})
        print(meaning_chinese_raw)
        return meaning_chinese_raw
    except:
        function_failed_statement()
        pass


def get_mp3(soup):
    try:
        mp3_file = soup.find("source", {"type": "audio/mpeg"})["src"]
        base_url = "https://dictionary.cambridge.org"
        mp3_url = base_url + mp3_file
        return mp3_url
    except:
        function_failed_statement()
        pass


#soup = get_soup(text)
soup = get_soup(text1)
#meaning_chinese = get_meaning_chinese(soup)
meaning = get_meaning_PartOfSpeech_eg(soup)
#mp3_url = get_mp3(soup)
