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

def crawlGmarket(keyword, driver):
    titleList = []
    priceList = []
    multiPriceList = []
    deliverList = []
    hrefList = []
    
    shopList = []
    shopNameList = []
    
    titlePath = 'div.box__item-title > span.text__item-title.text__item-title--ellipsis > a.link__item > span.text__item'
    pricePath = 'div.box__item-price > div.box__price-seller > strong.text.text__value'
    ulPath = 'div.box__component.box__component-itemcard.box__component-itemcard--general'
    hrefPath = 'div.box__item-title > span.text__item-title.text__item-title--ellipsis > a.link__item'
    
    
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=option)
    driver.get('http://browse.gmarket.co.kr/search?keyword='+keyword+'&f=is:cb&s=8')
    
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    try:
        
        ulList = soup.select(ulPath)
        titles = ulList[0].select(titlePath)
        prices = ulList[0].select(pricePath)
        hrefs  = ulList[0].select(hrefPath)
        
        for title in titles:
            textTitle = title.get_text()
            #print(textTitle)
            try: titleList.append(textTitle)
            except: pass
    
        for price in prices:
            textPrice = price.get_text()
            #print(textPrice)
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
        rest_post(keyword,'local','Gmarket',titleList[0],int(priceList[0]),hrefList[0],0,shopNameList,multiPriceList)    
    except: pass
    
    print(f'상품이름: {titleList}')
    print(f'대표가격: {priceList}')
    print(f'바로가기 링크: {hrefList}')