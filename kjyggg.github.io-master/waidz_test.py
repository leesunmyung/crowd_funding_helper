from selenium import webdriver
from selenium.common.exceptions import *
import time
from selenium.webdriver.common.action_chains import ActionChains
import csv
import pandas as pd


path ="C:/Users/User/almaden Dropbox/Al maden/wadiz_git/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get('https://www.wadiz.kr/web/campaign/detail/57507')

time.sleep(1)
driver.implicitly_wait(1)

elem = driver.find_element_by_xpath("//div[@class='btn-wrap funding']")
elem.click()

time.sleep(1)
driver.implicitly_wait(1)

id_box = driver.find_element_by_xpath("//input[@placeholder='이메일 아이디']")
id_box.send_keys('')#아이디입력
password_box = driver.find_element_by_xpath("//input[@placeholder='비밀번호(영문, 숫자, 특수문자 포함 8자 이상)']")
password_box.send_keys('')#비밀번호입력
login = driver.find_element_by_xpath("//button[@id='btnLogin']")
login.click()

time.sleep(1)
driver.implicitly_wait(1)

check1 = driver.find_element_by_xpath("//*[@id='reward-notice-form']/dl/dt[1]/label/span")
check1.click()
check2 = driver.find_element_by_xpath("//*[@id='reward-notice-form']/dl/dt[2]/label/span")
check2.click()
check3 = driver.find_element_by_xpath("//*[@id='reward-notice-form']/dl/dt[3]/label/span")
check3.click()
btn_continue = driver.find_element_by_xpath("//*[@id='btn-continue-funding']")
btn_continue.click()

price_funding= driver.find_element_by_xpath("//*[@id='purchaseForm']/div[1]/div[2]/ul/li[1]/dl/dd/label/p[1]")
name= driver.find_element_by_xpath("//*[@id='purchaseForm']/div[1]/div[2]/ul/li[1]/dl/dd/label/p[2]")
remains= driver.find_element_by_xpath("//*[@id='purchaseForm']/div[1]/div[2]/ul/li[1]/dl/dd/label/p[2]/em")
info= driver.find_element_by_xpath("//*[@id='purchaseForm']/div[1]/div[2]/ul/li[1]/dl/dd/label/p[3]")
date= driver.find_element_by_xpath("//*[@id='purchaseForm']/div[1]/div[2]/ul/li[1]/dl/dd/label/p[4]")

print(price_funding.text)
print(name.text)
print(remains.text)
print(info.text)
print(date.text)