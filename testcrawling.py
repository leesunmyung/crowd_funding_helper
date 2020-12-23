
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
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='0000',
                               db='test', charset='utf8')

        #self.path = os.path.dirname(os.path.realpath(__file__))
        print('DB connected')
        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.driver = webdriver.Chrome(options=option, executable_path=self.path + "\chromedriver.exe")


    def getUrlLister(self, page_url, nUrl):

        #chromedriver = 'C:/Users/ljy01/Desktop/chromedriver/chromedriver_win32/chromedriver.exe'
        #driver = webdriver.Chrome(chromedriver)
        SCROLL_PAUSE_TIME = 4

        self.driver.get(page_url)
        time.sleep(SCROLL_PAUSE_TIME)

        conn = self.conn
        curs = conn.cursor()


        # Get scroll height
#        last_height = driver.execute_script("return document.body.scrollHeight")
        last_height = 0

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #print('down')
            time.sleep(SCROLL_PAUSE_TIME)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000);")
            #print('up')
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        for i in range(1, nUrl+1):
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div['+str(i)+']/div/div/div[3]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[2]/div/div/div[3]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[3]/div/div/div[3]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[4]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[5]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[6]/div/div/div[3]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[7]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[8]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[9]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[10]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[11]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[12]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[13]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[14]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[15]/div/div/div[2]/a
            #//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div[16]/div/div/div[2]/a
            try:
                xpath1 = '//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div['+str(i)+']/div/div/div[2]/a'
                url = self.driver.find_element_by_xpath(xpath1)
                url = url.get_attribute('href')
            except:
                xpath1 = '//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div['+str(i)+']/div/div/div[3]/a'
                url = self.driver.find_element_by_xpath(xpath1)
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
        #conn.close()
    def goToCommunityTab(self):



    def tumblbugCrawler(self):
        conn = self.conn
        curs = conn.cursor()

        sql = "select * from tumblbug_urllist where crawled='F' or crawled='DB insert error'"
        curs.execute(sql)
        rows = curs.fetchall()

        #self.driver = self.webdriver.Chrome(options=option, executable_path=self.path + "\chromedriver.exe")
        #chromedriver = 'C:/Users/ljy01/Desktop/chromedriver/chromedriver_win32/chromedriver.exe'
        #driver = webdriver.Chrome(chromedriver)

        for row in rows:
            id = row[0]
            pagename = "tumblbug"#row[2]
            url = row[1]

            if url == 'None':
                continue;

            self.driver.get(url)
            sub_html = self.driver.page_source

            sub_soup = BeautifulSoup(sub_html, 'html.parser')
            sub_html = self.driver.page_source

            sub_soup = BeautifulSoup(sub_html, 'html.parser')

            projectName = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > div.ProjectIntroduction__ProjectOutline-sc-1o2ojgb-2.jbdzfG > div > h1')
            brand = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > div.ProjectIntroduction__ProjectOutline-sc-1o2ojgb-2.jbdzfG > div > div > a')
            Category = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > div.ProjectIntroduction__ProjectOutline-sc-1o2ojgb-2.jbdzfG > div > a > span')
            collection = sub_soup.find('div',attrs={'class': 'ProjectIntroduction__StatusValue-sc-1o2ojgb-16 lgJcVA'})
            remain_day = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-13.jqTlEc > div:nth-child(2) > div.ProjectIntroduction__StatusValue-sc-1o2ojgb-16.lgJcVA')
            percentachieved = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-13.jqTlEc > div:nth-child(1) > div.ProjectIntroduction__StatusValue-sc-1o2ojgb-16.lgJcVA > span.ProjectIntroduction__FundingRate-sc-1o2ojgb-17.cNDicH')
            goal = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > aside > div.FundingInformation-cjd67l-0.gGtZns > div > span')
            pagename = "tumblbug"

            print("success1\n")
            #category
            for i in Category:
                category = i.text.strip()
            category = category.replace(" ","")

            #title
            for i in projectName:
                title = i.text.strip()

            #brand
            for i in brand:
                Brand = i.text.strip()

            #achieve
            for i in percentachieved:
                pt = i.text.strip()
            ptnum = len(pt)
            achieve = pt[:ptnum-1]

            #funding - 달성 금액
            for tag in collection(['span']):
                tag.replace_with('')
            funding = collection.text.replace(",","")

            supporter = "tobe"

            # likes = NULL

            # goal
            for i in goal:
                notsplit = i.text.strip()
            split1 = notsplit.split("목표 금액인")
            split2 = split1[1].split('원이')
            goalmoney = split2[0].replace(",","").replace(" ","")

            #remaining
            for i in remain_day:
                day = i.text.strip()
            daynum = len(day)
            remaining = day[:daynum-1]

            #endate - 수작업
            endate = "tobe"
            print("success2\n")

            sql1 = 'insert into tumblbug_crawl (id, pagename, category, title, achieve, funding, supporter, goal,remaining, endate)                                                    value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'                                                        %(id, pagename, category, title, achieve, funding, supporter, goal, remaining, endate)
            curs.execute(sql1)
            conn.commit()
            print("success3\n")
            print('Crawling '+url+' finish',sql1)

            conn.commit()
            sql_url = "update tumblbug_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
            curs.execute(sql_url)
            conn.commit()

            goToCommunityTab()


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

if __name__ == '__main__':

    page_url = 'https://tumblbug.com/discover?ongoing=onGoing&sort=endedAt'
    nUrl = 100
    wc = TumblbugCrawler()
    wc.getUrlLister(page_url, nUrl)
    wc.tumblbugCrawler()


# In[ ]:
