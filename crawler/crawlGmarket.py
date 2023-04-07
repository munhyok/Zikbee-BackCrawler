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
from crawler.rest import rest_post


userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
option = Options()

option.add_argument("user-agent="+userAgent)
option.add_argument("lang=ko_KR")
#option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("disable-gpu")


def crawlGmarket(keyword, driver): #11번가
    
    
    
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(os_type="mac_arm64").install()),options=option)
    driver.get('https://browse.gmarket.co.kr/search?keyword='+keyword+'&s=8&f=is:cb')
    doScrollDown(100,driver)
    time.sleep(3)
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')


    items = soup.select('div.section__module-wrap > div.box__component.box__component-itemcard.box__component-itemcard--general')
    #print(items)
    
    indexList = []
    
    for idx, item in enumerate(items):
        
        img = 'https:'+item.find('img', attrs={'class':'image__item'})['src']
        title = item.find('span', attrs={'class':'text__item'})['title']
        price = int(filtering_string(item.find('div', attrs={'class':'box__item-price'}).find('div', attrs={'class':'box__price-seller'}).find('strong').get_text()))
        try:
            deliver = item.find('span', attrs={'class':'text__tag'}).find('img')['alt']
            if deliver == '무료배송': deliver = 0
        except:
            deliver = int(filtering_string(item.find('span', attrs={'class':'text__tag'}).get_text()))
        #review = item.find('ul', attrs={'class':'list__score'}).find('li', attrs={'class':'list-item.list-item__feedback-count'}).find('span', attrs={'class':'text'}).get_text()
        href = item.find('a', attrs={'class':'link__item'})['href']
        
        print('-'*30)
        print("img: {}".format(img))
        print("title : {}".format(title))
        print("price : {}".format(price))
        print("deliver : {}".format(deliver))
        #print("review: {}".format(review))
        print("가격+배송비: {}".format(int(price)+deliver))
        
        if idx < 10:
            indexList.append([title,price,deliver,price+deliver,img,href])
        
    
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
    
    try:
        print(indexsrt[0])
        rest_post(keyword,'local','Gmarket',indexsrt[0][0],indexsrt[0][1],indexsrt[0][2],indexsrt[0][3],indexsrt[0][4], indexsrt[0][5])
    except:
        pass
    
    