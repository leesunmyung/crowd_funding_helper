import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
import time
from urllib.request import urlopen
from lxml import etree
import pymysql
from datetime import datetime
import re
from selenium.webdriver import ActionChains

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

##########Wadiz crawling############
#####Wadiz Reward 카테고리별 크롤링하기

#wadiz reward 페이지
###popup control###
class WadizCrawler:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='wdta2181',
                               db='test', charset='utf8mb4')

        self.path = os.path.dirname(os.path.realpath(__file__))

        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })

        self.driver = webdriver.Chrome(options=option, executable_path=self.path+"\chromedriver.exe")
        self.driver.implicitly_wait(3)
        #self.driver.get('https://www.wadiz.kr/web/wreward/main?keyword=&endYn=ALL&order=recent')

    def extractCol(self,tree, category, title, achieve, funding, supporter, goal, period, remaining):

        try:
            category = category[0]
        except:
            category = 'None'
        try:
            title = title[0]
        except:
            title = 'None'
        try:
            achieve = achieve[0]
        except:
            achieve = 'None'
        try:
            supporter = supporter[0]
        except:
            supporter = 'None'
        """
        try:
            likes = likes[0]
        except:
            likes = 'None'
        """
        try:
            funding = funding[0]
        except:
            funding = 'None'
        try:
            goal = goal[0][:-1]
        except:
            goal = 'None'

        try:
            period = period[0].strip()
        except:
            period = 'None'

        try:
            remaining = remaining[0]
            #remaining = remaining[0][:-4]
            #print(remaining)
        except:
            remaining = 'None'
            """
        try:
            stdate = period.split('-')[0].replace('.', '-')
        except:
            stdate = 'None'
            """
        try:
            endate = period.split('-')[1].replace('.', '-')
        except:
            endate = 'None'
        return category, title, achieve, funding, supporter, goal, period, remaining, endate

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
            print('cleaser error!!')
            text = 'None'
        return text

    def getUrlLister(self, pagename, page_url, nUrl):

        option = Options()

        option.add_argument("--disable-infobars")
        option.add_argument("start-maximized")
        option.add_argument("--disable-extensions")

        # Pass the argument 1 to allow and 2 to block
        option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2
        })

        self.driver = webdriver.Chrome(options=option, executable_path=self.path + "\chromedriver.exe")
        self.driver.get(page_url)

        conn = self.conn
        curs = conn.cursor()

        n_scrollDown = nUrl//48 + 2
        k=0
        while k<n_scrollDown+1:
            k+=1
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            print(str(k)+"번 반복했습니다.")

        for i in range(1, nUrl+1):
            xpath ='/html/body/div[1]/main/div[2]/div/div[3]/div[2]/div[1]/div[%d]/div/div/a'%(i)
            url = self.driver.find_element_by_xpath(xpath)
            url = url.get_attribute('href')

            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            brand = soup.select('#main-app > div.MainWrapper_content__GZkTa > div > div.RewardProjectListApp_container__1ZYeD > div.ProjectCardList_container__3Y14k > div.ProjectCardList_list__1YBa2 > div:nth-child('+str(i)+') > div > div > div > div > div.RewardProjectCard_infoTop__3QR5w > div > span.RewardProjectCard_makerName__2q4oH')[0]
            brand = brand.get_text()
            brand = self.cleansing(brand)

            sql0 = "select * from wadiz_urllist where url=\'%s\'" % (url)
            curs.execute(sql0)
            rows = curs.fetchall()
            status = 'F'
            if len(rows)==0:
                sql= "insert into wadiz_urllist(url, pagename, crawled, brand) values (\'%s\',\'%s\',\'%s\',\'%s\')"%(url, pagename, status, brand)
                curs.execute(sql)
                conn.commit()

            print(i, url)
            #url = url.get_attribute('href')
            #print(url)
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        conn.close()

    def getCrawler(self):

        conn = self.conn
        curs = conn.cursor()

        #크롤링 안된 url 가져오기
        sql = "select * from wadiz_urllist where crawled='F' or crawled='DB insert error'"
        curs.execute(sql)
        rows = curs.fetchall()

        #크롤링이 안된 모든 행들에 대해서 실시
        for row in rows:
            # id, pagename, url 을 urllist 에서 가져온다
            id = row[0]
            pagename = row[1]
            url = row[2]
            if url == 'None':
                continue

            # 해당 url 을 이용해서 requests 하고 요소들을 가져온다.
            response = urlopen(url)
            htmlparser = etree.HTMLParser()
            tree = etree.parse(response, htmlparser)

            category = tree.xpath('//*[@id="container"]/div[3]/p/em/text()')
            title = tree.xpath('//*[@id="container"]/div[3]/h2/a/text()')

            achieve = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[3]/strong/text()')
            funding = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[4]/strong/text()')
            supporter = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[5]/strong/text()')
            #likes1 = list(tree.xpath('//*[@id="cntLike"]/text()')[0])
            #likes1 = "".join(likes1)
            #likes = []
            #likes.append(likes1)
            goal = tree.xpath(
                '//*[@id="container"]/div[6]/div/div[1]/div[2]/div/div/section/div[4]/div/div[5]/div/p[1]/text()[2]')
            #goal = goal[0][:-1]
            #print(goal)
            #print('goal=', goal[0])
            #goal1 = goal[0][:-1]
            #print('goal1=', goal1)
            period = tree.xpath(
                '//*[@id="container"]/div[6]/div/div[1]/div[2]/div/div/section/div[4]/div/div[5]/div/p[1]/text()[4]')
                #period에서 펀딩 기간을 가져와야하는데 목표 금액이 갖고 와짐..
            remaining = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[1]/text()')


            try:
                if remaining[0] == '% 달성':
                    funding = tree.xpath(
                        '//*[@id="container"]/div[4]/div/div[1]/div[2]/div/div/section/div[4]/div/div[1]/div[1]/p[2]/strong/text()')
                    supporter = tree.xpath(
                        '//*[@id="container"]/div[4]/div/div[1]/div[2]/div/div/section/div[4]/div/div[1]/div[1]/p[3]/strong/text()')
                    likes = tree.xpath('//*[@id="cntLike"]/text()')
            except:
                print('url:',url)

            now = datetime.now()
            dtStr = now.strftime("%Y-%m-%d %H:%M:%S")

            category, title, achieve, funding, supporter, goal, period, remaining, endate = self.extractCol(tree, category, title,achieve, funding, supporter, goal, period, remaining)

            category = self.cleansing(category)
            title = self.cleansing(title)

            achieve = self.cleansing(achieve)
            funding = self.cleansing(funding)
            supporter = self.cleansing(supporter)
            #likes = self.cleansing(likes)
            goal = self.cleansing(goal)
            period = self.cleansing(period)
            remaining = self.cleansing(remaining)
            #endate = self.cleansing(endate)
            nowday = now.strftime("%Y-%m-%d")

                # sql3 = "update wadiz_urllist set crawled='DB insert Error' where url=\'%s\'" % (url)
                # curs.execute(sql3)
                # conn.commit()
                # print('first', id, pagename, category, title, achieve, funding, supporter, likes, goal, period, remaining, stdate, endate, dtStr, url)
            # url 을 통해 가져온 내용들을 crawl 테이블에 저장한다.
            # id 를 통해
            sql0 = "select count(*) from wadiz_crawl where id = %d and remaining_day=\'%s\'"% (id, remaining)

            curs.execute(sql0)
            row = curs.fetchall()
            if row[0][0]==0:
                try:
                    if endate>nowday:
                        remaining = remaining[:-4]
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                                                    %(id, pagename, category, title, achieve, funding, supporter, goal, remaining, endate)
                        curs.execute(sql1)
                        conn.commit()

                        print('Crawling '+url+' finish',sql1)

                        conn.commit()
                        sql_url = "update wadiz_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
                        curs.execute(sql_url)
                        conn.commit()

                    elif remaining=='펀딩성공':
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                                        value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                               % (
                               id, pagename, category, title, achieve, funding, supporter, goal,
                               remaining, endate)
                        curs.execute(sql1)
                        conn.commit()
                        print('Crawling ' + url + ' finish', sql1)

                        sql_url = "update wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()
                    else:
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                                        value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                               % (
                               id, pagename, category, title, achieve, funding, supporter, goal,
                               '0', endate)
                        curs.execute(sql1)
                        conn.commit()
                        print('Crawling ' + url + ' finish', sql1)

                        sql_url = "update wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()
                except:
                    sql0 = "update wadiz_urllist set crawled='DB insert Error' where url=\'%s\'"%(url)
                    curs.execute(sql0)
                    conn.commit()
                    print('second',sql0, url)

                print("Get User Info")

                replacedUrl = url

                if '?' in url:
                    replacedUrl = url.split('?')[0]
                if 'detail' in url:
                    replacedUrl = url.replace('detail','detailBacker')
                if 'wcomingsoon' in url:
                    replacedUrl = url.replace('wcomingsoon/rwd','campaign/detailBacker')
                self.driver.get(replacedUrl)
                self.driver.implicitly_wait(30)
                print("replaced url: "+replacedUrl)
                Num = self.driver.find_element_by_xpath('//*[@id="container"]/div[6]/div/div/div[1]/div[1]/div[1]/p[5]/strong')
                self.driver.implicitly_wait(30)
                supporterNum = Num.text
                if len(supporterNum) >= 4 :
                    supporterNum = supporterNum.strip().replace(',', '')

                n = 1;
                while True:
                    try:
                        more_xpath = self.driver.find_element_by_xpath('//*[@id="reward-static-supports-list-app"]/div/div/div/div[2]/button')

                        action = ActionChains(self.driver).click()
                        action.move_to_element(more_xpath).perform()
                        #self.driver.find_element_by_xpath('//*[@id="reward-static-supports-list-app"]/div/div/div/div[2]/button').click()
                        n = n+1;
                        #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                        print("더보기", n, "번 누름")
                        self.driver.implicitly_wait(30)

                    except:
                        print("더보기 끝")
                        break;


                for i in range(1, int(supporterNum)+1):
                    user_xpath = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/button'%i
                    anonymous = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/strong[1]'%i
                    investment_xpath = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/strong'%i
                    self.driver.implicitly_wait(30)

                    try:
                        user = self.driver.find_element_by_xpath(user_xpath).text
                    except:
                        user = '익명의 서포터'

                    self.driver.implicitly_wait(30)
                    investment = self.driver.find_element_by_xpath(investment_xpath).text
                    self.driver.implicitly_wait(30)

                    if user != '익명의 서포터' and investment != '지지서명' and investment != '펀딩':
                        user = self.cleansing(user)
                        investment = investment[:-4]
                        sql= "insert into wadiz_user_info(site, title, username, investment) values ('wadiz',\'%s\',\'%s\',\'%s\')"%(title, user, investment)
                        curs.execute(sql)
                        conn.commit()
                    elif investment == '펀딩' :
                        user = self.cleansing(user)
                        if remaining == '펀딩성공' :
                            defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button[1]/div/dl/dt'
                        else :
                            defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[8]/div/button[1]/div/dl/dt'
                        investment = self.driver.find_element_by_xpath(defaultoption_xpath).text
                        investment = investment[:-4]
                        sql= "insert into wadiz_user_info(site, title, username, investment) values ('wadiz',\'%s\',\'%s\',\'%s\')"%(title, user, investment)
                        curs.execute(sql)
                        conn.commit()
                    else :
                        continue
        else:
            print(url+"already exist")

        conn.close()
