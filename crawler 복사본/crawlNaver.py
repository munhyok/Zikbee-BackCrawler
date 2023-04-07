from audioop import mul
from distutils.log import error
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




def crawlNaver(keyword,driver): #네이버
    
    
    titlePath = 'div.basicList_title__VfX3c > a.basicList_link__JLQJf'
    pricePath = 'strong.basicList_price__euNoD > span > span.price_num__S2p_v'
    deliverPath = 'span.deliveryInfo_info_delivery__3DAnV'
    
    smartStorePath = 'div.basicList_mall_title__FDXX5 > a.basicList_mall__BC5Xu' 
    multiShopPath = 'ul.basicList_mall_list__S_B5C > li > a.basicList_mall_item__bFc5i' #title, #href
    multiPricePath = 'ul.basicList_mall_list__S_B5C > li > a.basicList_mall_item__bFc5i > span.basicList_price__euNoD'
    singleShopPath = 'div.basicList_mall_title__FDXX5 > a.basicList_mall__BC5Xu > img' #alt
    
    ulPath = 'ul.list_basis > div > div > li.basicList_item__0T9JD'
    
    singlePrice = 0
    
    
    titleList = []
    priceList = []
    multiPriceList = []
    deliverList = []
    hrefList = []
    
    shopList = []
    shopNameList = []
    
    #driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=option)
    driver.get('https://search.shopping.naver.com/search/all?frm=NVSHOVS&origQuery='+keyword+'&pagingIndex=1&pagingSize=80&productSet=overseas&query='+keyword+'&sort=review&timestamp=&viewType=list')
    driver.implicitly_wait(10)
    #doScrollDown(100,driver)
    
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    
    
    
    
    try:
        ulList = soup.select(ulPath)
        titles = ulList[0].select(titlePath)
        prices = ulList[0].select(pricePath)
        delivers = ulList[0].select(deliverPath)
        hrefs = ulList[0].select(titlePath)
        
        
        singleShops = ulList[0].select(singleShopPath)
        multiShops = ulList[0].select(multiShopPath)
        smartStores = ulList[0].select(smartStorePath)
        multiPrices = ulList[0].select(multiPricePath)
        
        
        
        
        for title in titles:
            titleText = title.get_text()
            titleList.append(titleText)
        
        for price in prices:
            priceText = price.get_text()
            price_ = filtering_string(priceText)
            priceList.append(int(price_))
            singlePrice = int(price_)

        
        
        for deliver in delivers:
            deliverText = deliver.get_text()
            filterText = filtering_string(deliverText)
            if filterText == '무료': filterText = 0
            deliverList.append(filterText)
            
        
        if deliverList == []: deliverList.append(0)

        for href in hrefs:
            hrefText = href.get('href')
            hrefList.append(hrefText)



        for single in singleShops:
                singleName = single.get('alt')
                #print(singleName)
                try: shopNameList.append(singleName)
                except: pass

        if len(shopNameList) == 0:
            try:

                    for multi in multiShops:
                        multiTitle = multi.get('title')
                        multiHref = multi.get('href')
                        #multi.get_text()
                        #print(multiTitle)
                        try: shopNameList.append(multiTitle)
                        except: pass

                        #print(multi.get_text())
                    for multiPrice in multiPrices:
                        price = multiPrice.get_text()
                        #print(price)
                        try: multiPriceList.append(price)
                        except: pass

            except:

                pass


        try:
            for smartStore in smartStores:
                smartStoreText = smartStore.get_text()
                try:
                    shopNameList.append(smartStoreText)
                    shopNameList.pop(1)
                except: pass
        except:
            pass
        
    except:
        print('오류 혹은 상품없음')
        pass
    
    
    
    

    
    
    print(f'상품이름: {titleList}')
    print(f'대표가격: {priceList}')
    print(f'배송비: {deliverList}')
    print(f'여러쇼핑몰: {shopNameList}')
    print(f'여러쇼핑몰 가격: {multiPriceList}')
    
    print(f'바로가기 링크: {hrefList}')
    print(f'싱글 프라이스 {singlePrice}')
    
        
    try:
        rest_post(keyword,'local','Naver',titleList[0],singlePrice,hrefList[0],int(deliverList[0]),shopNameList,multiPriceList)
    except:
        pass
    
    
    #time.sleep(10)
    #driver.close()