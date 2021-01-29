import time
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from selenium.webdriver.chrome.options import Options
import os
from urllib.request import urlopen
from lxml import etree
import pymysql
from datetime import datetime
import re



class TumblbugCrawler:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='wdta2181',
                               db='test', charset='utf8')

        self.path = os.path.dirname(os.path.realpath(__file__))
        print('DB connected')

    def getUrlLister(self, page_url, nUrl):
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })
        driver = webdriver.Chrome(options=option, executable_path=self.path + "\chromedriver.exe")
        SCROLL_PAUSE_TIME = 4

        driver.get(page_url)
        time.sleep(SCROLL_PAUSE_TIME)

        conn = self.conn
        curs = conn.cursor()


        # Get scroll height
#        last_height = driver.execute_script("return document.body.scrollHeight")
        last_height = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #print('down')
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            #print('up')
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight-300);")
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[2]/a
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div/dl/dt/a

#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[3]/a
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div/dl/dt/a

#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div/div[2]/a
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div/dl/dt/a


        for i in range(1, nUrl+1):
            xpath1 = '//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div['+str(i)+']/div/div/dl/dt/a'
            url = driver.find_element_by_xpath(xpath1)
            url = url.get_attribute('href')
            sql0 = "select * from tumblbug_urllist where url=\'%s\'" % (url)
            curs.execute(sql0)
            rows = curs.fetchall()
            status = 'F'
            if len(rows)==0:
                sql= "insert into tumblbug_urllist(url, crawled) values (\'%s\',\'%s\')"%(url,status)
                curs.execute(sql)
                conn.commit()

                print(i,url)
                    #url = url.get_attribute('href')
                    #print(url)
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        conn.close()

"""
        n_scrollDown = nUrl//18+2
        k=0
        while k<n_scrollDown+1:
            k+=1
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if k == n_scrollDown:
                break
            last_height = new_height
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
            print(str(k)+"번 반복했습니다.")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
"""
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[1]/div/div/div[3]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[2]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div/div[2]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[4]/div/div/div[3]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[5]/div/div/div[3]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[6]/div/div/div[2]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[7]/div/div/div[2]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[8]/div/div/div[2]/a/img
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[18]/div/div/dl/dt/a
#//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[19]/div/div/dl/dt/a


if __name__ == '__main__':

    page_url = 'https://tumblbug.com/discover?ongoing=onGoing&sort=endedAt'
    nUrl = 100
    wc = TumblbugCrawler()
    wc.getUrlLister(page_url, nUrl)
