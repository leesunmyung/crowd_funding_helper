import requests
import bs4
from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
import time
from urllib.request import urlopen
from lxml import etree
import pymysql
from datetime import datetime
import re

class SevenCrawler:

    def __init__(self):
        self.conn = pymysql.connect(host='106.246.169.202', user='root', password='robot369', db='crawl', charset='utf8mb4')
        self.path = os.path.dirname(os.path.realpath(__file__))

    def getReview(self):
        page_url = 'https://apps.apple.com/kr/app/%EC%84%B8%EB%B8%90%EB%82%98%EC%9D%B4%EC%B8%A0/id741949324#see-all/reviews'

        # option = Options()
        #
        # option.add_argument("--disable-infobars")
        # option.add_argument("start-maximized")
        # option.add_argument("--disable-extensions")
        #
        # # Pass the argument 1 to allow and 2 to block
        # option.add_experimental_option("prefs", {
        #     "profile.default_content_setting_values.notifications": 2
        # })
        # driver = webdriver.Chrome(options=option, executable_path=self.path + "\chromedriver.exe")
        # driver.get(page_url)

        r = requests.get(page_url)
        r = r.text
        soup = bs4.BeautifulSoup(r, 'html.parser')
        print(soup)
        # point = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/div/span[1]/div/div')
        # id = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/span')
        # review = driver.find_element_by_xpath('//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/span[1]')
        # '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div[2]/div[2]/span[1]'
        # '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[2]/div/div[2]/div[2]/span[1]'
        # '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/span[1]'
        # review = review.text
        # id = id.text
        # point = point.get_attribute('aria-label')
        # point = point.split(' ')[3][0]
        # print(point)
        # print(review, id)
        # category = tree.xpath('//*[@id="container"]/div[2]/p/em/text()')
#        while True:
#            conn = self.conn
#
#            time.sleep(0.5)
#            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#            xpath = '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div'
#            try:
#                button = driver.find_element_by_xpath(xpath)
#                button.click()
#            except:
#                None


