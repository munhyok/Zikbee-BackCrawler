import asyncio
import multiprocessing
import queue
import websockets
from requests.structures import CaseInsensitiveDict
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

from datetime import date
from datetime import datetime
import datetime

from multiprocessing import Pool, Process, Queue, Pipe
import multiprocessing as mp
import subprocess
import os
import time

from crawler.crawlbot import crawlbot

    
async def accept(websocket, path):
    while True:
        data = await websocket.recv()
        print(data)
        await websocket.send(data)
        
        p = Process(target=crawlbot, args=(data ,))
        p.start()
        p.join
        
        
    

if __name__=='__main__':

    asyncio.get_event_loop().run_until_complete(websockets.serve(accept, "127.0.0.1", 1212))
    asyncio.get_event_loop().run_forever()
    



    