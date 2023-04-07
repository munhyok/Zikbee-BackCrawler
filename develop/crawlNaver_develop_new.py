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



def crawlNaver(): #네이버
    
    keyword = '나이키 CW2288-111'
    
    indexList = []
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(os_type="mac_arm64").install()),options=option)
    driver.get('https://search.shopping.naver.com/search/all?frm=NVSHOVS&origQuery='+keyword+'&pagingIndex=1&pagingSize=80&productSet=overseas&query='+keyword+'&sort=review&timestamp=&viewType=list')
    driver.implicitly_wait(10)
    doScrollDown(500,driver)
    
    time.sleep(2)
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    
    items = soup.find_all("li", attrs={"class":"basicList_item__0T9JD"})
    
    print(items)
    
    for idx, item in enumerate(items):
        
        img = item.find("a", attrs={"class":"thumbnail_thumb__Bxb6Z"}).find("img")["src"]
        title = item.find("a", attrs={"class":"basicList_link__JLQJf"})["title"]
        price = int(filtering_string(item.find("span", attrs={"class":"price_num__S2p_v"}).get_text()))
        try:
            filter_deliver = filtering_string(item.find("span", attrs={"class":"deliveryInfo_info_delivery__3DAnV"}).get_text())
            deliver = int(filter_deliver)
        except AttributeError:
            deliver = 0
            
        review = item.find('em', attrs={"class":"basicList_num__sfz3h"}).get_text()
        
        href = item.find("a", attrs={"class":"basicList_link__JLQJf"})["href"]
        
        
        
        print('-'*30)
        print("img: {}".format(img))
        print("title : {}".format(title))
        print("price : {}".format(price))
        print("deliver : {}".format(deliver))
        print("review : {}".format(review))
        print()
        if deliver == '알 수 없음':
            print("가격+배송비: {}".format(price))
        else: print("가격+배송비: {}".format(int(price)+deliver))
        
        
        if idx < 10:
            indexList.append([title,price,deliver,price+deliver,img, href])
        
    
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
crawlNaver()