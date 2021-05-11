from selenium import webdriver

import requests

base_url = "https://dictionary.cambridge.org/dictionary/english-chinese-traditional/"
option = webdriver.ChromeOptions()
option.add_argument('headless')

print("What you want to search?")
input_word = "fish"
webpage = base_url + input_word

webdriver_path = r"D:\Code\Website\seminar_E_learning_system\web_scraping\chromedriver.exe"

browser = webdriver.Chrome(executable_path=webdriver_path, options=option)
browser.get(webpage)

audio_url = browser.find_element_by_xpath(
    "/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[4]/div/div/div[1]/div[2]/span[2]/span[2]/amp-audio/audio/source[1]")
print("++++++++")
print(audio_url.get_attribute("src"))

browser.quit()
