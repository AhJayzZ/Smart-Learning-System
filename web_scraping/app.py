from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


options = Options()
options.add_argument("--disable-notifications")

chrome = webdriver.Chrome(
    r"D:/Code/Website/seminar_E_learning_system/web_scraping/chromedriver.exe", chrome_options=options)
chrome.get("https://www.facebook.com/")

email = chrome.find_element_by_id("email")
password = chrome.find_element_by_id("pass")

email.send_keys('choongtuckwai21@gmail.com')
password.send_keys('ac611k079')
password.submit()

for x in range(1, 4):
    chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(5)
