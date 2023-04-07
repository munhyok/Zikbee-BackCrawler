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

def crawlAmazon(keyword, driver):
    
    titleList = []
    priceList = []
    multiPriceList = []
    deliverList = []
    hrefList = []
    
    shopList = []
    shopNameList = []
    
    titlePath = 'span.a-size-base-plus.a-color-base.a-text-normal'
    pricePath = 'div.a-row.a-size-base.a-color-base > a > span > span > span.a-price-whole'
    ulPath = 'div.a-section.a-spacing-base'
    hrefPath = 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal'
    deliverPath = 'div.a-section.a-spacing-none.a-spacing-top-micro > div.a-row.a-size-base.a-color-secondary.s-align-children-center > span > span.a-color-base'
    
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=option)
    
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
    
    
    driver.get('https://www.amazon.com/s?k='+keyword+'&crid=3RC97W4Y0IJSN&sprefix=%2Caps%2C255&ref=nb_sb_ss_recent_1_0_recent')
    time.sleep(1)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    
    
    #print(ulList[0])

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
            print(textPrice)
            try: priceList.append(filtering_string(textPrice))
            except: pass

        for href in hrefs:
            textHref = href.get('href')
            try: hrefList.append('https://www.amazon.com'+textHref)
            except: pass
    except:
        print('오류 혹은 상품 없음')
        pass
    #delivers = ulList[0].select(deliverPath)
    
    
        
    #for deliver in delivers:
    #    deliverText = deliver.get_text()
    #    print(deliverText)
    #    filterText = filtering_string(deliverText)
    #    print(filterText)
    #    deliverList.append(filterText)
    
    
    print(f'상품이름: {titleList}')
    print(f'대표가격: {priceList}')
    print(f'바로가기 링크: {hrefList}')
    
    try:    
        rest_post(keyword,'overseas','Amazon',titleList[0],int(priceList[0]),hrefList[0],0,shopNameList,multiPriceList)
    
    except IndexError:
        try:
            rest_post(keyword,'overseas','Amazon',titleList[0],0,hrefList[0],0,shopNameList,multiPriceList)

        except:
            pass
    
    