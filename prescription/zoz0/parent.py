from . import constant as const
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.edge.service import Service
from msedge.selenium_tools import EdgeOptions, Edge


class PARENT:
    _instance = None
    
    def __init__(self):
        if not PARENT._instance:
            # set up options for headless browsing
            options = EdgeOptions()
            options.use_chromium = True
            # options.add_argument('--headless')
            # options.add_argument('--disable-infobars')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument('--disable-browser-side-navigation')
            # options.add_argument('--disable-gpu')
            # options.add_argument('--no-sandbox')

            driver_path = r"D:\msedgedriver.exe"
            self.driver = Edge(options=options, executable_path=driver_path)
            
            self.wait = WebDriverWait(self.driver,poll_frequency=1,timeout= 2)

            PARENT._instance = self
        else:
            self.driver = PARENT._instance.driver
            self.wait = PARENT._instance.wait

    
        
    
    def open(self):
        pass  # headless mode doesn't require opening the browser

    def landFirstPage(self , URL = const.BASE_URL):
        self.driver.get(URL)
    
    def search(self, drug_name):
        print('first')
        element = self.wait.until(EC.element_to_be_clickable((By.ID, 'livesearch-main')))
        print('first')
        element.clear()
        print('first')
        element.send_keys(drug_name, Keys.ENTER)
        print('first')
    
    def back(self):
        script = "return window.history.back()"
        self.driver.execute_script(script)

    
    def hashing(self,txt):
        hash=0
        for i in range(len(txt)):
            hash = (hash+ord(txt[i]) * 13** (len(txt)-i-1) ) % 1000000031
        return hash
    
    
    def closePopUp(self,clas='ddc-modal-close'):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, clas)))
            element.click()
        except:
            print('not here')
    
    def closeSmallPopUp(self):
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fc-close']")))
            element.click()
            print('closed')
        except:
            print('not here')

