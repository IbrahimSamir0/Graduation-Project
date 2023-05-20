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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class PARENT:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # # set up options for headless browsing
            options = EdgeOptions()
            options.use_chromium = True
            options.add_argument('--headless')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            capabilities = DesiredCapabilities.EDGE
            capabilities["pageLoadStrategy"] = "eager"


            driver_path = r"D:\msedgedriver.exe"
            cls.driver = Edge(options=options,executable_path=driver_path, desired_capabilities=capabilities)
            
            # cls.wait = WebDriverWait(cls.driver, 2)

        return cls._instance
    
    
    
    
    def open(self):
        pass  # headless mode doesn't require opening the browser

    def landFirstPage(self , URL = const.BASE_URL):
        self.driver.get(URL)
    
    def search(self, drug_name):
        
        element = self.driver.find_element(By.ID, 'livesearch-main')
        element.clear()
        element.send_keys(drug_name, Keys.ENTER)
    
    def back(self):
        script = "return window.history.back()"
        self.driver.execute_script(script)

    
    def closeSmallPopUp(self):
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.XPATH, "//button[@class='fc-close']")))
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fc-close']")))
            element.click()
            print('closed')
        except:
            print('not here')
    
    def closePopUp(self,clas='ddc-modal-close'):
        try:
            WebDriverWait(self.driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, clas)))
            element = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, clas)))
            element.click()
            print('closed')
        except:
            print('not here')
    
    def hashing(self,txt):
        hash=0
        for i in range(len(txt)):
            hash = (hash+ord(txt[i]) * 13** (len(txt)-i-1) ) % 1000000031
        return hash
