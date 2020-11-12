from selenium import webdriver
from urllib.request import urlopen
import time
from lxml import etree
import re
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import os
option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {
    "profile.default_content_setting_values.notifications": 2
})

path = os.path.dirname(os.path.realpath(__file__))
driver = webdriver.Chrome(options=option, executable_path=path+"\chromedriver.exe")

page_url = 'https://www.wadiz.kr/web/wreward/main?keyword=&endYn=ALL&order=recent'
driver.get(page_url)
login_button = driver.find_element_by_xpath('//*[@id="main-app"]/div[1]/div/header/div/div/div[2]/div/div[1]/button[1]')
login_button.click()
time.sleep(0.5)
putid = driver.find_element_by_xpath('//*[@id="userName"]')
putid.send_keys("vasana12@naver.com")
putpass = driver.find_element_by_xpath('//*[@id="password"]')
putpass.send_keys("ahfmsek2!")
login = driver.find_element_by_xpath('//*[@id="btnLogin"]')
login.click()

time.sleep(1)
page_url2 = 'https://www.wadiz.kr/web/campaign/detail/32090'
driver.get(page_url2)

funding_button = driver.find_elements_by_xpath('//*[@id="container"]/div[4]/div/div[1]/div[1]/div[1]/div[2]/button')[0]
funding_text = funding_button.text
print(funding_text)
funding_button.click()
time.sleep(2)

checkbox1 = driver.find_element_by_xpath('//*[@id="reward-notice-form"]/dl/dt[1]/label')
checkbox1.click()

checkbox2 = driver.find_element_by_xpath('//*[@id="reward-notice-form"]/dl/dt[2]/label')
checkbox2.click()

checkbox3 = driver.find_element_by_xpath('//*[@id="reward-notice-form"]/dl/dt[3]/label')
checkbox3.click()

checkbox4 = driver.find_element_by_xpath('//*[@id="reward-notice-form"]/dl/dt[4]/label')
checkbox4.click()

funding = driver.find_element_by_xpath('//*[@id="btn-continue-funding"]')
funding.click()
time.sleep(0.5)
test = driver.find_elements_by_class_name('reward-box')
for i in test :
    price_list = i.find_element_by_tag_name('dd').text

    print(price_list)

#for i in price_list:
#   print(i.text)
#response = urlopen('https://www.wadiz.kr/web/campaign/detail/56049')
#htmlparser = etree.HTMLParser()
#tree = etree.parse(response, htmlparser)
#early_bird = tree.xpath('/html/body/div[1]/div[4]/div/div[2]/form/div[1]/div[2]/ul/li[1]/dl/dd/input[1]')
#print(early_bird)

