# Import Package
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

print("What you want to search?")
input_word = input()
#input_word = "fish"

# Chrome.exe location set
options = Options()
options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# WebDriver Path
webdriver_path = r"D:\Code\Website\seminar_E_learning_system\web_scraping\chromedriver.exe"

# Enabled Chrome function 打開模擬瀏覽器
chrome_browser = webdriver.Chrome(
    executable_path=webdriver_path, options=options)

target_web = "https://dictionary.cambridge.org/zht/%E8%A9%9E%E5%85%B8/%E8%8B%B1%E8%AA%9E-%E6%BC%A2%E8%AA%9E-%E7%B9%81%E9%AB%94/"

# go to the website
chrome_browser.get(target_web + input_word)
meaning = chrome_browser.find_element_by_xpath(
    "/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[4]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[3]/span")
part_of_speech = chrome_browser.find_element_by_xpath(
    "/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[4]/div/div/div[1]/div[2]/div[2]/span")

examp = chrome_browser.find_element_by_xpath(
    "/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[4]/div/div/div[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[1]/span[1]")

print(part_of_speech.text)
print(meaning.text)
print(examp.text)

# Close down the website
chrome_browser.close()
