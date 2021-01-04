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
from datetime import timedelta
import re
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
#import calendar

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

class TumblbugCrawler:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='wdta2181',
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

        SCROLL_PAUSE_TIME = 4
        IMPLICITLY_PAUSE_TIME = 120

        self.driver.get(page_url)
        time.sleep(SCROLL_PAUSE_TIME)

        conn = self.conn
        curs = conn.cursor()

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        self.driver.execute_script("window.scrollTo( document.body.scrollHeight, document.body.scrollHeight-2000);")
        time.sleep(SCROLL_PAUSE_TIME)
        time.sleep(20)

        #n_url = 1161
        for i in range(1, nUrl+1):
            try:
                xpath1 = '//*[@id="react-view"]/div[3]/div[1]/div[2]/div/div[2]/div['+str(i)+']/div/div/div[2]/a'
                url = self.driver.find_element_by_xpath(xpath1)
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


    def getuserinfo(self, url, title):
        #스크롤 하는 코드 추가.
        conn = self.conn
        curs = conn.cursor()

        print("Get User Info - tumblbug")
        url = url.replace("?","/community?")

        self.driver.get(url)

        print("is there any posting?")
        try:
            communityPostNum = self.driver.find_element_by_xpath('//*[@id="contentsNavigation"]/nav/div/div/a[2]/span').text
            self.driver.implicitly_wait(5)
            print("yes, there are ", end='')
            print(communityPostNum)
        except:
            print("no")
            return

        #커뮤니티 숫자가 5 이상이면 스크롤 내려본다.
        if int(communityPostNum) >= 5 :
            print('communityPostNum : ', int(communityPostNum))
            SCROLL_PAUSE_TIME = 2
            # Get scroll height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                last_height = new_height

        projectHost = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[5]/div[1]/div/div[2]/div/div[1]/div/div[2]/a/span').text

        for i in range(2, int(communityPostNum)+2):
            try:
                user = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[5]/div[1]/div/div[1]/div/div/div/div['+str(i)+']/div/div[1]/div/div/div[1]/div/a/div').text
                #print(user,end='')

                if user != projectHost :
                    try :       #진행 중인 프로젝트.
                        investment = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[5]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/section[1]/div/div[2]/div/div/div[1]').text
                    except :
                        try :   #진행 중인 프로젝트.('n개 남음' 박스 있음)
                            investemnt = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[6]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/section[1]/div/div[2]/div/div/div[1]').text
                        except :
                            try :   #펀딩 성공[6] or 펀딩무산[6] or 펀딩 중단.
                                investment = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[6]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]').text
                            except :
                                try :   #펀딩 성공[5] or 펀딩 무산[5].
                                    investment  = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[5]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]').text
                                except :
                                    #try :   #펀딩 중단.
                                    #    investment = self.driver.find_element_by_xpath('//*[@id="react-view"]/div[6]/div[1]/div/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div/div/div[1]').text
                                    #except :
                                    print("investment 없음")
                                    return

                    investment = self.cleansing(investment)
                    investment = re.sub('[^0-9]','',investment)
                    print(user, investment)

                    sql = "insert into tumblbug_user_info(site, title, username, investment) values ('tumblbug',\'%s\',\'%s\',\'%s\')"%(title, user, investment)
                    curs.execute(sql)
                else :
                    continue
            except:
                continue

            conn.commit()



    def cleansing(self, text):
        try:
            text = re.sub('[ㅣ,#/:$@*\"※&%ㆍ』\\‘|\(\)\[\]\<\>`\'…》]', '', text)

            text = re.sub(r'\\', '', text)
            text = re.sub(r'\\\\', '', text)
            text = re.sub('\'', '', text)
            text = re.sub('\"', '', text)

            text = re.sub('\u200b', ' ', text)
            text = re.sub('&nbsp;|\t', ' ', text)
            text = re.sub('\r\n', '\n', text)

            while (True):
                text = re.sub('  ', ' ', text)
                if text.count('  ') == 0:
                    break

            while (True):
                text = re.sub('\n \n ', '\n', text)
                # print(text.count('\n \n '))
                if text.count('\n \n ') == 0:
                    break

            while (True):
                text = re.sub(' \n', '\n', text)
                if text.count(' \n') == 0:
                    break

            while (True):
                text = re.sub('\n ', '\n', text)
                if text.count('\n ') == 0:
                    break

            while (True):
                text = re.sub('\n\n', '\n', text)
                # print(text.count('\n\n'))
                if text.count('\n\n') == 0:
                    break
            text = re.sub(u'[\u2500-\u2BEF]', '', text)  # I changed this to exclude chinese char

            # dingbats
            text = re.sub('\\-|\]|\{|\}|\(|\)', "", text)

            text = re.sub(u'[\u2702-\u27b0]', '', text)
            text = re.sub(u'[\uD800-\uDFFF]', '', text)
            text = re.sub(u'[\U0001F600-\U0001F64F]', '', text)  # emoticons
            text = re.sub(u'[\U0001F300-\U0001F5FF]', '', text)  # symbols & pictographs
            text = re.sub(u'[\U0001F680-\U0001F6FF]', '', text)  # transport & map symbols
            text = re.sub(u'[\U0001F1E0-\U0001F1FF]', '', text)  # flags (iOS)
        except Exception as e:
            print('cleaser error')
            text = 'None'
        return text

    def tumblbugCrawler(self):
        #funding, achieve int형으로 바꾸기.
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
            url = row[2]

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
            supporter = sub_soup.select('#react-view > div.ProjectIntroduction__ProjectIntroductionBackground-sc-1o2ojgb-0.gsZkXT > div > div > aside > div.ProjectIntroduction__FundingStatus-sc-1o2ojgb-13.jqTlEc > div:nth-child(3) > div.ProjectIntroduction__StatusValue-sc-1o2ojgb-16.lgJcVA')
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
                global Brand
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


            #supporter = "tobe"

            for i in supporter :
                supporternum = i.text.strip()
            supporter = supporternum[:-1]
            supporter = supporter.replace(',', '')

            # likes = NULL

            # goal
            for i in goal:
                notsplit = i.text.strip()

            split = notsplit.split(' ')
            if split[2][-1] == '게' or split[2][-1] == '지':  #선물전달 or 펀딩 무산(실패).
                goalmoney = str(int(int(funding) / (int(achieve)/100)))
                print('선물 전달 혹은 펀딩 무산 프로젝트의 goal:', goalmoney)
            elif split[2][-1] == '을' or split[2][-1] == '이' :   #펀딩성공 or 진행중.
                goalmoney = split[2][:-2].replace(",", "")
                print('펀딩 성공 혹은 진행중 프로젝트의 goal:', goalmoney)
            elif split[2][-1] == '의' :  #펀딩 중단.
                sql_del = "delete tumblbug_urllist set where id = %d"%id
                sql_up = "update tumblbug_urllist set id = id-1 where id >= %d"%(id)
                curs.execute(sql_del)
                conn.commit()
                curs.execute(sql_up)

                conn.commit()
                continue

            #split1 = notsplit.split("목표 금액인")
            #split2 = split1[1].split('원이')
            #goalmoney = split2[0].replace(",","").replace(" ","")

            #remaining
            for i in remain_day:
                day = i.text.strip()
            daynum = len(day)
            remaining = day[:daynum-1]
            if remaining[-1] == '시' :
                remaining = remaining[:-1]

            #endate - 수작업
            #펀딩 진행중인 프로젝트에서는 오늘 날짜에 remaining_day 더해 구한다.
            if int(remaining) >= 1 :
                now = datetime.now()
                endate = now + timedelta(days=int(remaining))
                endate = endate.strftime("%Y-%m-%d")
                #endate= self.cleansing(endate) #cleansing 하면 대쉬(-) 사라짐.
                print(endate)

            #펀딩 성공한 프로젝트에서는 회색 상자에서 가져온다.
            elif split[2][-1] == '을' :
                endate = ''.join(split[4:7])
                print(endate)   #2021년1월1일에
                #endate = endate.replace(' ', '')
                endate = endate.replace('에', '')
                endate = endate.replace('일', '')
                endate = endate.replace('년', '-')
                endate = endate.replace('월', '-')
                #2021-1-1
                if endate[6] == '-' :
                    #5자리에 0넣기. #2021-01-1
                    endate = endate[:5] + '0' + endate[5:]
                if len(endate) == 9 :
                    #8자리에 0넣기
                    endate = endate[:8] + '0' + endate[8:]
                print(endate)
            else :
                endate = "tobe"

            pagename = self.cleansing(pagename)
            category = self.cleansing(category)
            title= self.cleansing(title)
            Brand = self.cleansing(Brand)
            achieve= self.cleansing(achieve)
            funding= self.cleansing(funding)
            supporter= self.cleansing(supporter)
            goalmoney= self.cleansing(goalmoney)
            remaining= self.cleansing(remaining)
            #endate= self.cleansing(endate)


            print("success2\n")

            sql1 = 'insert into tumblbug_crawl (id, pagename, category, title, brand, achieve, funding, supporter, goal,remaining_day, endate)\
                                                values(%d,\'%s\',\'%s\',\'%s\',\'%s\', \'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                                                    %(id, pagename, category, title, Brand, achieve, funding, supporter, goalmoney, remaining, endate)
            curs.execute(sql1)
            conn.commit()

            print("success3\n")
            print('Crawling '+url+' finish',sql1)

            conn.commit()

            if id <= 242 :
                sql_url = "update tumblbug_urllist set status='펀딩중', crawled='T', brand=\'%s\' where url=\'%s\'"% (Brand, url)  #where id -> where url
                curs.execute(sql_url)
                conn.commit()
            elif id >=243 & id <= 1000 :
                sql_url = "update tumblbug_urllist set status='펀딩완료', crawled='T', brand=\'%s\' where url=\'%s\'"% (Brand, url)  #where id -> where url
                curs.execute(sql_url)
                conn.commit()
            else :
                return

            self.getuserinfo(url, title)

        conn.close()



if __name__ == '__main__':

    #page_url = 'https://tumblbug.com/discover?ongoing=onGoing&sort=endedAt'
    #page_url = 'https://tumblbug.com/discover?currentMoney=2&sort=publishedAt'  #백만원~천만원, 최신순. 1000개.
    #page_url = 'https://tumblbug.com/discover?achieveRate=1&currentMoney=2&sort=publishedAt'    #백만원~천만원, 75%이하, 최신순. 100개.
    #page_url = 'https://tumblbug.com/discover?achieveRate=1&currentMoney=3&sort=publishedAt'    #천만원~오천만원, 75%이하, 최신순. 20개.
    #page_url = 'https://tumblbug.com/discover?currentMoney=4&sort=publishedAt'   #오천만원~일억원, 최신순. 150개.
    #page_url = 'https://tumblbug.com/discover?currentMoney=5&sort=publishedAt'   #일억원 이상, 최신순. 60개.

    nUrl = 100
    wc = TumblbugCrawler()
    #wc.getUrlLister(page_url, nUrl)
    wc.tumblbugCrawler()
