from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from datetime import date
from datetime import datetime
import datetime

from multiprocessing import Pool, Process, Queue, Pipe
import multiprocessing as mp
import subprocess
import os
import time


from doScrollDown import doScrollDown
from filterString import filtering_string



userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
option = Options()

option.add_argument("user-agent="+userAgent)
option.add_argument("lang=ko_KR")
#option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("disable-gpu")


def crawlAmazon(): #11번가
    
    keyword = '나이키 에어포스 1'
    
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(os_type="mac_arm64").install()),options=option)
    
    
    driver.get('https://www.amazon.com/customer-preferences/edit?ie=UTF8&preferencesReturnUrl=%2Fref%3Dnav_logo&ref_=topnav_lang_ais')
    
    try:
        driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/form/div[1]/div[1]/div[7]/div/label/span').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/form/div[3]/div/p/span/span/span/span').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/ul/li[9]/a').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/span[2]/span').click()
        time.sleep(3)
    except:
        driver.get('https://www.amazon.com/customer-preferences/edit?ie=UTF8&preferencesReturnUrl=%2Fref%3Dnav_logo&ref_=topnav_lang_ais')
        
        driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/form/div[1]/div[1]/div[7]/div/label/span').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/form/div[3]/div/p/span/span/span/span').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div/ul/li[9]/a').click()
        time.sleep(0.5)
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/span[2]/span').click()
        time.sleep(3)
    
    
    
    
    driver.get('https://www.amazon.com/s?k='+keyword)
    #doScrollDown(50,driver)
    time.sleep(2)
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')


    items = soup.select('div.a-section.a-spacing-base')
    #print(items)
    
    indexList = []
    
    for idx, item in enumerate(items):
        
        
        img = item.find('img', attrs={'class':'s-image'}).get('src')
        title = item.find('img', attrs={'class':'s-image'})['alt']
        
        try:
            price = int(filtering_string(item.find('span', attrs={'class':'a-price-whole'}).get_text()))
        except: price = 0
        
        deliver = 0
        
        try:
            href = item.select_one('a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').get('href')
        except AttributeError:
            href = item.select_one('a.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal')['href']
        href = 'https://amazon.com'+href
        
        
        print('-'*30)
        print("img: {}".format(img))
        print("title : {}".format(title))
        print("price : {}".format(price))
        print("deliver : {}".format(deliver))
        #print("review: {}".format(review))
        print("가격+배송비: {}".format(int(price)+deliver))
        print("href :{}".format(href))
        
        if price != 0:
            if idx < 10:
                indexList.append([title,price,deliver,price+deliver,img,href])
        
    time.sleep(1)
    driver.close()
    #
    #
    print('='*60)
    print(indexList)
    print(len(indexList))
    print('='*60)
    print('배송비 포함 가격 낮은순')
    indexsrt = sorted(indexList,key=lambda x: x[3])
    print(indexsrt)
    print()
    print('최종 최저가')
    print(indexsrt[0])

crawlAmazon()