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
import requests
import json

from doScrollDown import doScrollDown
from filterString import filtering_string
from crawler.crawlGmarket import crawlGmarket
from crawler.crawlAmazon import crawlAmazon
from crawler.crawlEleven import crawlEleven
from crawler.crawlNaver import crawlNaver
from crawler.rest import rest_post



userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
option = Options()

option.add_argument("user-agent="+userAgent)
option.add_argument("lang=ko_KR")
#option.add_argument('headless')
option.add_argument('window-size=1920x1080')
option.add_argument("disable-gpu")

ulPath, titlePath, pricePath, deliverPath = '','','',''
smartStorePath, multiShopPath, multiPricePath, singleShopPath = '','','',''




def crawlbot(keyword):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(os_type="mac_arm64").install()),options=option) #https://github.com/SergeyPirogov/webdriver_manager/issues/446
    crawlNaver(keyword, driver)
    crawlEleven(keyword, driver)
    crawlGmarket(keyword, driver)
    crawlAmazon(keyword, driver)
    
    send_data = rest_post('','','','','','','','','')
    send_data = json.dumps(send_data, indent=4, ensure_ascii=False).encode('utf-8')
    
    print(send_data.decode())

    headers = {'Content-Type': 'application/json'}
    response = requests.post('http://127.0.0.1:5200/goods', data=send_data)
    print(response.status_code)
    print(response.reason)
    
    
    
    driver.quit()
    
    