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


l_marketList, l_titleList, l_shopList, l_priceList, l_deliverList, l_shopsList, l_pricesList = [],[],[],[],[],[], []
o_marketList, o_titleList, o_priceList, o_deliverList, o_shopsList, o_pricesList = [],[],[],[],[],[]
#DB POST Variable

data = {
        
            "keyword": "검색키워드",
            "path": "goods",
            "crawlstate": False,
            "local": [
              
            ],
            "overseas": [
              
            ]

    }


def rest_post(keyword, section ,market, title, price, deliver, totalPrice, href, img):
    
    
    if keyword == '':
        return data
    else:
    
        data["keyword"] = keyword

        if section == 'local':

            data["local"].append({"market":market,"goodsname":title,"price":price,"deliver":deliver,"totalprice":totalPrice,"href":href, "img":img})


        elif section == 'overseas':
   
            data["overseas"].append({"market":market,"goodsname":title,"price":price,"deliver":deliver,"totalprice":totalPrice,"href":href, "img":img})

        else: pass

        #print(data)

        