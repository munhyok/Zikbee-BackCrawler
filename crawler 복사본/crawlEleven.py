from audioop import mul
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
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.chrome.options import Options

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

def crawlEleven(keyword, driver): #11번가
    titlePath = 'div.c_prd_name.c_prd_name_row_1 > a > strong'
    pricePath = 'div.c_prd_price > dl.price > dd > span.value'
    ulPath = 'ul.c_listing.c_listing_view_type_list > li > div.c_card.c_card_list'
    hrefPath = 'div.c_prd_name.c_prd_name_row_1 > a'
    
    titleList = []
    priceList = []
    multiPriceList = []
    deliverList = []
    hrefList = []
    
    shopList = []
    shopNameList = []
    
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=option)
    driver.get('https://search.11st.co.kr/Search.tmall?kwd='+keyword+'&fromACK=recent#sortCd%%SPS%%11%EB%B2%88%EA%B0%80%20%EC%9D%B8%EA%B8%B0%EC%88%9C%%14$$pageNum%%1%%page%%19$$filterPrdState%%GLOBAL_DIRECT%%%ED%95%B4%EC%99%B8%EC%A7%81%EA%B5%AC%%18')
    time.sleep(3)
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    
    try:
        ulList = soup.select(ulPath)


        titles = ulList[0].select(titlePath)
        prices = ulList[0].select(pricePath)
        hrefs  = ulList[0].select(hrefPath)
        
        for title in titles:
            textTitle = title.get_text()
            print(textTitle)

            try: titleList.append(textTitle)
            except: pass
    
        for price in prices:
            textPrice = price.get_text()
            print(textPrice)
            try: priceList.append(filtering_string(textPrice))
            except: pass
        for href in hrefs:
            textHref = href.get('href')
            try: hrefList.append(textHref)
            except: pass
        
    except:
        print('오류 혹은 상품 없음')
        pass
    
    try:
        rest_post(keyword,'local','11st',titleList[0],int(priceList[0]),hrefList[0],0,shopNameList,multiPriceList)
    except: pass
    
    print(f'상품이름: {titleList}')
    print(f'대표가격: {priceList}')
    print(f'바로가기 링크: {hrefList}')
    
    
    time.sleep(3)
    #driver.close()