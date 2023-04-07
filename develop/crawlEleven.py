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


def crawlEleven(): #11번가
    
    keyword = '나이키 CW2288-111'
    
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(os_type="mac_arm64").install()),options=option)
    driver.get('https://search.11st.co.kr/Search.tmall?kwd='+keyword+'&fromACK=recent#sortCd%%SPS%%11%EB%B2%88%EA%B0%80%20%EC%9D%B8%EA%B8%B0%EC%88%9C%%14$$pageNum%%1%%page%%19$$filterPrdState%%GLOBAL_DIRECT%%%ED%95%B4%EC%99%B8%EC%A7%81%EA%B5%AC%%18')
    time.sleep(2)
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')


    items = soup.select('ul.c_listing.c_listing_view_type_list > li')
    
    indexList = []
    
    for idx, item in enumerate(items):
        
        img = item.find('img')['src']
        title = item.find('strong').get_text()
        price = int(filtering_string(item.find('span', attrs={'class':'value'}).get_text()))
        deliver = int(filtering_string(item.find('span', attrs={'class':'delivery'}).get_text()))
        review = '0'
        href = item.find('a')['href']
        print('-'*30)
        print("img: {}".format(img))
        print("title : {}".format(title))
        print("price : {}".format(price))
        print("deliver : {}".format(deliver))
        print("href: {}".format(href))
        
        
        if idx < 10:
            indexList.append([title,price,deliver,price+deliver,img, href])
        
    time.sleep(1)
    driver.close()
    
    
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

crawlEleven()