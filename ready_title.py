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
                               db='test', charset='utf8')

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
            achieve = '0'
        try:
            supporter = supporter[0]
        except:
            supporter = '0'
        """
        try:
            likes = likes[0]
        except:
            likes = 'None'
        """
        try:
            funding = funding[0]
        except:
            funding = '0'
        try:
            goal = goal[0][1:-1]
        except:
            goal = '0'

        try:
            period = period[0].strip()
        except:
            period = 'None'

        try:
            remaining = remaining[0]
            #remaining = remaining[0][:-4]
            #print(remaining)
        except:
            remaining = '0'
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
        #wadiz_urllist에 url 넣기.
        #wadiz_crawl에 brand 넣기.

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
        SCROLL_PAUSE_TIME = 4
        IMPLICITLY_PAUSE_TIME = 120

        self.driver.get(page_url)
        time.sleep(SCROLL_PAUSE_TIME)

        conn = self.conn
        curs = conn.cursor()


        time.sleep(30)

        """
        n_scrollDown = nUrl//48 + 2
        k=0
        while k<n_scrollDown+1:
            k+=1
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            print(str(k)+"번 반복했습니다.")
        """

        id = 5925    #id
        for i in range(30, 101):
            if i == 100 or id == 5975 :
                return

            #xpath ='/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[%d]/div/div/a'%(i) #종료된 프로젝트.
            xpath ='/html/body/div[1]/main/div[2]/div/div[3]/div[2]/div[1]/div[%d]/div/div/a'%(i) #진행중 프로젝트.

            url = self.driver.find_element_by_xpath(xpath)
            url = url.get_attribute('href')

            """
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            brand = soup.select('#main-app > div.MainWrapper_content__GZkTa > div > div.RewardProjectListApp_container__1ZYeD > div.ProjectCardList_container__3Y14k > div.ProjectCardList_list__1YBa2 > div:nth-child('+str(i)+') > div > div > div > div > div.RewardProjectCard_infoTop__3QR5w > div > span.RewardProjectCard_makerName__2q4oH')[0]
            brand = brand.get_text()
            brand = self.cleansing(brand)
            """
            #/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[1875]/div/div/div/div/div[1]/div/span[2]
            #/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[2566]/div/div/div/div/div[1]/div/span[2]
            brand_xpath = '/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[' + str(i) + ']/div/div/div/div/div[1]/div/span[2]'   #종료된 프로젝트.
            brand_xpath = '/html/body/div[1]/main/div[2]/div/div[3]/div[2]/div[1]/div[' + str(i) + ']/div/div/div/div/div[1]/div/span[2]'   #진행중 프로젝트.

            brand = self.driver.find_element_by_xpath(brand_xpath)
            brand = brand.text
            brand = self.cleansing(brand)

            print('id : ', id, ', div[', i, '], url : ', url, ', brand : ', brand)

            sql0 = "select * from wadiz_urllist where url=\'%s\'" % (url)
            curs.execute(sql0)
            rows = curs.fetchall()
            status = 'F'

            sql1 = "select * from urllist where url=\'%s\'" % (url)
            curs.execute(sql1)
            rows1 = curs.fetchall()

            #wadiz_urllist에 url 넣기.
            if len(rows) == 0 and len(rows1) == 0:
                sql= "insert into test.wadiz_urllist(id, url, pagename, crawled, status) values (%d, \'%s\',\'%s\',\'%s\',\'%s\')"%(id, url, pagename, status, status)
                #sql= "insert into wadiz_urllist(url, pagename, crawled, brand) values (\'%s\',\'%s\',\'%s\',\'%s\')"%(url, pagename, status, brand)
                curs.execute(sql)
                conn.commit()
                print('wadiz_urllist 들어감, ', 'id : ', id, ', div[', i, '], url : ', url, ', brand : ', brand)

                #wadiz_crawl에 brand 넣기.
                sql_brand = "insert into test.wadiz_crawl (id, brand) values (%d, \'%s\')"%(id, brand)
                curs.execute(sql_brand)
                conn.commit()
                print('wadiz_crawl 들어감, ', 'id : ', id, ', brand : ', brand)

                #url 하나 들어갔으니 id 번호 증가 시켜야 함.
                id = id + 1


        conn.close()

    def getCrawler(self):
        flag = 0;
        conn = self.conn
        curs = conn.cursor()

        #self.manipulateDB()

        #크롤링 안된 url 가져오기
        #sql = "delete from wadiz_urllist where title "
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

            period = tree.xpath(
                '//*[@id="container"]/div[6]/div/div[1]/div[2]/div/div/section/div[4]/div/div[5]/div/p[1]/text()[4]')

            remaining = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[1]/text()')

            try:
                #펀딩 기간 지났고, 펀딩 성공 못한 프로젝트. flag=1;
                if remaining[0] == '% 달성':
                    print(remaining[0])
                    flag=1;
                    remaining = '0'
                    print("펀딩기간/펀딩성공 안적혀있는 프로젝트 url : ", url)
                    achieve = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[1]/strong/text()')
                    funding = tree.xpath(
                        '//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[2]/strong/text()')
                    supporter = tree.xpath(
                        '//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[3]/strong/text()')
                    #likes = tree.xpath('//*[@id="cntLike"]/text()')
            except:
                print('00일 남음 또는 펀딩 성공 url:',url)

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
            print('goal : ', goal)
            period = self.cleansing(period)
            remaining = self.cleansing(remaining)
            print("remaining : ", remaining)
            #endate = self.cleansing(endate)
            nowday = now.strftime("%Y-%m-%d")


            # url 을 통해 가져온 내용들을 crawl 테이블에 저장한다.
            # id 를 통해
            sql0 = "select count(*) from wadiz_crawl where id = %d and remaining_day=\'%s\'"% (id, remaining)

            curs.execute(sql0)
            row = curs.fetchall()
            if row[0][0]==0:
                try:
                    #아직 기간 남은 경우.
                    #오늘 자정 마감인 경우는 endate==nowday라서 제외.
                    if endate>nowday :
                        remaining = remaining[:-4]
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                                                    %(id, pagename, category, title, achieve, funding, supporter, goal, remaining, endate)
                        curs.execute(sql1)
                        conn.commit()

                        print(remaining, '일 남음 : ', 'Crawling '+url+' finish',sql1)

                        conn.commit()
                        sql_url = "update wadiz_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
                        curs.execute(sql_url)
                        conn.commit()

                    elif endate == nowday : #remaining=='오늘 자정 마감'
                        remaining = '1';
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'\
                                                    %(id, pagename, category, title, achieve, funding, supporter, goal, remaining, endate)
                        curs.execute(sql1)
                        conn.commit()

                        print('오늘 자정 마감 : ', 'Crawling '+url+' finish',sql1)

                        conn.commit()
                        sql_url = "update wadiz_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
                        curs.execute(sql_url)
                        conn.commit()

                    #기간 지났고, 펀딩은 성공한 프로젝트.. '펀딩 성공'이라고 뜨는 경우.
                    elif remaining=='펀딩성공':
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                                        value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                               % (
                               id, pagename, category, title, achieve, funding, supporter, goal,
                               '0', endate)
                        curs.execute(sql1)
                        conn.commit()
                        print('펀딩성공(기간 지남(0)) : ', 'Crawling ' + url + ' finish', sql1)

                        sql_url = "update wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()

                    #기간도 지났고, 펀딩 성공하지 못한 프로젝트. 그래서 위에 아무것도 안뜨는 경우. remaining_day는 0으로.
                    else :
                        sql1 = 'insert into wadiz_crawl (id, pagename, category, title, achieve, funding, supporter, goal, remaining_day, endate)\
                                                                        value(%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')' \
                               % (
                               id, pagename, category, title, achieve, funding, supporter, goal,
                               '0', endate)
                        curs.execute(sql1)
                        conn.commit()
                        print('기간지났고 펀딩못함 : ', 'Crawling ' + url + ' finish', sql1)

                        sql_url = "update wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()
                except:
                    sql0 = "update wadiz_urllist set crawled='DB insert Error' where url=\'%s\'"%(url)
                    curs.execute(sql0)
                    conn.commit()
                    print('second',sql0, url)

                print("crawl end")
                """
                print("Get User Info")

                replacedUrl = url

                if '?' in url:
                    replacedUrl = url.split('?')[0]
                if 'detail' in url:
                    replacedUrl = url.replace('detail','detailBacker')
                if 'wcomingsoon' in url:
                    replacedUrl = url.replace('wcomingsoon/rwd','campaign/detailBacker')
                self.driver.get(replacedUrl)
                self.driver.implicitly_wait(20)
                print("replaced url: "+replacedUrl)

                print("supporter : ", supporter)


                #//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[501]/div/p/button

                #더보기 버튼 누르기.
                while True:
                    try:

                        more_xpath = self.driver.find_element_by_xpath('//*[@id="reward-static-supports-list-app"]/div/div/div/div[2]/button')
                        #more_xpath_text = self.driver.find_element_by_xpath('//*[@id="reward-static-supports-list-app"]/div/div/div/div[2]/button').text
                        #print(more_xpath_text, i)
                        action = ActionChains(self.driver).click()
                        action.move_to_element(more_xpath).perform()
                        #driver.find_element_by_xpath("//form[@class='ui form']/button").send_keys(Keys.ENTER)
                        time.sleep(1)
                        #self.driver.implicitly_wait(10)
                    except:
                        break

                for i in range(1, int(supporter)+1) :
                    #user_xpath = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/button'%i
                    user_xpath = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/button'%i

                    investment_xpath = '//*[@id="reward-static-supports-list-app"]/div/div/div/div[1]/div[%d]/div/p/strong'%i
                    self.driver.implicitly_wait(5)

                    try:
                        user = self.driver.find_element_by_xpath(user_xpath).text
                    except:
                        continue

                    #self.driver.implicitly_wait(10)
                    user = self.cleansing(user)
                    investment = self.driver.find_element_by_xpath(investment_xpath).text

                    #이선명님이 지지서명에 참여 했습니다.
                    if investment == '지지서명' :
                        continue

                    #이선명님이 펀딩에 참여했습니다.
                    elif investment == '펀딩' :
                        print(user, "그냥 펀딩")

                        #기간 지났고, '펀딩성공'도 아닌 경우라 위에 아무 것도 안뜨는 경우. 확산 안뜸.
                        if flag == 1 :
                            print("flag=1  ", user)
                            try :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button[1]/div/dl/dt'
                            except :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button/div/dl/dt'

                        #기간 지났고, '펀딩성공'이라고 뜨는 경우. 확산 안뜸.
                        elif remaining == '펀딩성공' :
                            try :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button[1]/div/dl/dt'
                            except :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button/div/dl/dt'

                        #아직 remaining_day가 남은 경우. 확산 뜸.
                        else :
                            try :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[8]/div/button[1]/div/dl/dt'
                            except :
                                defaultoption_xpath = '//*[@id="container"]/div[6]/div/div/div[1]/div[8]/div/button/div/dl/dt'

                        #성공 못함.
                        #리워드 1가지.
                        #//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button/div/dl/dt
                        #//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button/div/dl/dt
                        ##container > div.reward-body-wrap > div > div > div.wd-ui-sub-opener-info > div.moveRewards > div > button > div > dl > dt
                        #리워드 여러 개.
                        #//*[@id="container"]/div[6]/div/div/div[1]/div[7]/div/button[1]/div/dl/dt
                        ##container > div.reward-body-wrap > div > div.wd-ui-info-wrap > div.wd-ui-sub-opener-info > div.moveRewards > div > button:nth-child(3) > div > dl > dt

                        investment = self.driver.find_element_by_xpath(defaultoption_xpath).text
                        investment = investment.strip().replace(',', '')
                        investment = investment[:-4]
                        sql= "insert into wadiz_user_info(site, title, username, investment) values ('wadiz',\'%s\',\'%s\',\'%s\')"%(title, user, investment)

                    #이선명님이 30,000원 펀딩에 참여 했습니다.
                    else :
                        investment = investment.strip().replace(',', '')
                        investment = investment[:-4]
                        sql= "insert into wadiz_user_info(site, title, username, investment) values ('wadiz',\'%s\',\'%s\',\'%s\')"%(title, user, investment)

                    self.driver.implicitly_wait(10)

                    curs.execute(sql)
                    conn.commit()
                """
            flag = 0;   #새로운 프로젝트 들어가기 전 flag 초기화.
        else:
            print(url+"already exist")

        conn.close()


    def getBrand(self, page_url, nUrl):
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

        time.sleep(50)

        #html = self.driver.page_source
        #soup = BeautifulSoup(html, 'html.parser')

        #brand = soup.select('main-app > div.MainWrapper_content__GZkTa > div > div.RewardProjectListApp_container__1ZYeD.RewardMainProjectList_listApp__2noRS > div.ProjectCardList_container__3Y14k > div.ProjectCardList_list__1YBa2 > div:nth-child(3) > div > div > div > div > div.RewardProjectCard_infoTop__3QR5w > div > span.RewardProjectCard_makerName__2q4oH')
        #brand = self.driver.find_element_by_xpath('/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[3]/div/div/div/div/div[1]/div/span[2]')

#/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[1446]/div/div/div/div/div[1]/div/span[2]
#//*[@id="main-app"]/div[2]/div/div[5]/div[2]/div[1]/div[4]/div/div/div/div/div[1]/div/span[2] #키보드까지.
        for i in range(3971, 4975): #숫자바꿔야함.
            brand_xpath = '/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[' + str(i) + ']/div/div/div/div/div[1]/div/span[2]'
            brand = self.driver.find_element_by_xpath(brand_xpath)
            brand = brand.text
            brand = self.cleansing(brand)
            print(brand, i)

            sql = "update wadiz_crawl set brand = %s where id = %d"%(brand, i)
            curs.execute(sql)
            conn.commit()

            print("mysql 들어감", i, brand)

        #print(i, url)

        conn.close()


    def getCrawlerUpdate(self):
        flag = 0;
        conn = self.conn
        curs = conn.cursor()

        #self.manipulateDB()

        #크롤링 안된 url 가져오기
        #sql = "delete from wadiz_urllist where title "
        sql = "select * from wadiz_urllist where id >= 4975 "
        curs.execute(sql)
        rows = curs.fetchall()
        #print(rows)
        #크롤링이 안된 모든 행들에 대해서 실시
        for row in rows:
            # id, pagename, url 을 urllist 에서 가져온다
            id = row[0]
            print(id)
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

            period = tree.xpath(
                '//*[@id="container"]/div[6]/div/div[1]/div[2]/div/div/section/div[4]/div/div[5]/div/p[1]/text()[4]')

            remaining = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[1]/text()')

            try:
                #펀딩 기간 지났고, 펀딩 성공 못한 프로젝트. flag=1;
                if remaining[0] == '% 달성':
                    print(remaining[0])
                    flag=1;
                    remaining = '0'
                    print("펀딩기간/펀딩성공 안적혀있는 프로젝트 url : ", url)
                    achieve = tree.xpath('//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[1]/strong/text()')
                    funding = tree.xpath(
                        '//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[2]/strong/text()')
                    supporter = tree.xpath(
                        '//*[@id="container"]/div[6]/div/div[1]/div[1]/div[1]/div[1]/p[3]/strong/text()')
                    #likes = tree.xpath('//*[@id="cntLike"]/text()')
            except:
                print('00일 남음 또는 펀딩 성공 url:',url)

            now = datetime.now()
            dtStr = now.strftime("%Y-%m-%d %H:%M:%S")

            category, title, achieve, funding, supporter, goal, period, remaining, endate = self.extractCol(tree, category, title,achieve, funding, supporter, goal, period, remaining)
            print('endate:', endate)
            category = self.cleansing(category)
            title = self.cleansing(title)

            achieve = self.cleansing(achieve)
            funding = self.cleansing(funding)
            supporter = self.cleansing(supporter)
            #likes = self.cleansing(likes)
            goal = self.cleansing(goal)
            print('goal:', goal)
            period = self.cleansing(period)
            remaining = self.cleansing(remaining)
            print("remaining:", remaining)
            #endate = self.cleansing(endate)
            nowday = now.strftime("%Y-%m-%d")


            # url 을 통해 가져온 내용들을 crawl 테이블에 저장한다.
            # id 를 통해
            sql0 = "select count(*) from wadiz_crawl where id = %d and remaining_day=\'%s\'"% (id, remaining)

            curs.execute(sql0)
            row = curs.fetchall()
            if row[0][0]==0:
                try:
                    print("try들어옴")
                    #아직 기간 남은 경우.
                    #오늘 자정 마감인 경우는 endate==nowday라서 제외.
                    if endate>nowday :
                        print("endate>nowday")
                        remaining = remaining[:-4]
                        sql1 = 'update test.wadiz_crawl set pagename = \'%s\', category = \'%s\', title = \'%s\', achieve = \'%s\', funding = \'%s\', supporter = \'%s\', goal = \'%s\', remaining_day = \'%s\', endate = \'%s\' where id = %d'%(pagename, category, title, achieve, funding, supporter, goal, remaining, endate, id)
                        curs.execute(sql1)
                        conn.commit()

                        print(remaining, '일 남음 : ', 'Crawling '+url+' finish',sql1)

                        conn.commit()
                        sql_url = "update test.wadiz_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
                        curs.execute(sql_url)
                        conn.commit()

                    elif endate == nowday : #remaining=='오늘 자정 마감'
                        print("endate==nowday")
                        remaining = '1';
                        sql1 = 'update test.wadiz_crawl set pagename = \'%s\', category = \'%s\', title = \'%s\', achieve = \'%s\', funding = \'%s\', supporter = \'%s\', goal = \'%s\', remaining_day = \'%s\', endate = \'%s\' where id = %d'%(pagename, category, title, achieve, funding, supporter, goal, remaining, endate, id)
                        curs.execute(sql1)
                        conn.commit()

                        print('오늘 자정 마감 : ', 'Crawling '+url+' finish',sql1)

                        conn.commit()
                        sql_url = "update test.wadiz_urllist set status='펀딩중', crawled='T' where url=\'%s\'"% (url)  #where id -> where url
                        curs.execute(sql_url)
                        conn.commit()

                    #기간 지났고, 펀딩은 성공한 프로젝트.. '펀딩 성공'이라고 뜨는 경우.
                    elif remaining=='펀딩성공':
                        print("펀딩성공")
                        sql1 = 'update test.wadiz_crawl set pagename = \'%s\', category = \'%s\', title = \'%s\', achieve = \'%s\', funding = \'%s\', supporter = \'%s\', goal = \'%s\', remaining_day = \'%s\', endate = \'%s\' where id = %d' %(pagename, category, title, achieve, funding, supporter, goal, '0', endate, id)
                        curs.execute(sql1)
                        conn.commit()
                        print('펀딩성공(기간 지남(0)) : ', 'Crawling ' + url + ' finish', sql1)

                        sql_url = "update test.wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()

                    #기간도 지났고, 펀딩 성공하지 못한 프로젝트. 그래서 위에 아무것도 안뜨는 경우. remaining_day는 0으로.
                    else :
                        print("기간지났고펀딩못함")
                        sql1 = 'update test.wadiz_crawl set pagename = \'%s\', category = \'%s\', title = \'%s\', achieve = \'%s\', funding = \'%s\', supporter = \'%s\', goal = \'%s\', remaining_day = \'%s\', endate = \'%s\' where id = %d'%(pagename, category, title, achieve, funding, supporter, goal, '0', endate, id)
                        curs.execute(sql1)
                        conn.commit()
                        print('기간지났고 펀딩못함 : ', 'Crawling ' + url + ' finish', sql1)

                        sql_url = "update test.wadiz_urllist set status='펀딩완료',crawled='T' where url=\'%s\'" % (url)
                        curs.execute(sql_url)
                        conn.commit()
                except:
                    sql0 = "update wadiz_urllist set crawled='DB insert Error' where url=\'%s\'"%(url)
                    curs.execute(sql0)
                    conn.commit()
                    print('second',sql0, url)

                print("crawl end")

                """
                userinfo 필요 없으니 코드 삭제
                """

            flag = 0;   #새로운 프로젝트 들어가기 전 flag 초기화.
        else:
            print(url+"already exist")

        conn.close()

    def getBrandOnly(self, pagename, page_url) :
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

        self.driver.get(page_url)

        time.sleep(300)


        s = 1852
        for i in range(4623, 4975):
            sql = "select * from wadiz_urllist where id = %d"%i
            curs.execute(sql)
            conn.commit()
            rows = curs.fetchall()

            for row in rows:
                # id, pagename, url 을 urllist 에서 가져온다
                id = row[0]
                if i != id :
                    print('i랑 id가 다름 i :', i, 'id :', id)
                    return
                url_id = row[2]
                print('wadiz_urllist에서 id :', id, ' url :', url_id)

            for j in range(s, 2500) :
                xpath = '/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[%d]/div/div/a'%(j) #종료된 프로젝트.
                url_div = self.driver.find_element_by_xpath(xpath)
                url_div = url_div.get_attribute('href')

                if url_id == url_div :
                    brand_xpath = '/html/body/div[1]/main/div[2]/div/div[5]/div[2]/div[1]/div[' + str(j) + ']/div/div/div/div/div[1]/div/span[2]'   #종료된 프로젝트.
                    brand = self.driver.find_element_by_xpath(brand_xpath)
                    brand = brand.text
                    brand = self.cleansing(brand)

                    sql_brand = "update wadiz_crawl set brand = \'%s\' where id = %d"%(brand, i)
                    curs.execute(sql_brand)
                    conn.commit()
                    print("wadiz_crawl에 brand update함, id :", i, "j :", j, "brand :", brand)
                    s = j+1
                    break

                elif j - s > 30 :
                    print("10개 넘게 봤는데도 안나와서 비워두고 다음 id로 감")
                    break

                else :
                    print("아직 안나옴 j : ", j, "s:", s)
                    continue

        conn.close()
