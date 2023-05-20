from . import constant as const
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import  BeautifulSoup
# from selenium.webdriver.edge import service
import time
from selenium.webdriver.support.wait import WebDriverWait
from .D_B import DB


# ChromeDriverManager().install()


class PARENT(webdriver.Edge):
    instance = 0
    con = DB()

    def __init__(self):
        # edge_options = webdriver.EdgeOptions()
        # edge_options.add_argument('--headless')
        # caps = {"browserName": "MicrosoftEdge"}
        # edge_options.set_capability("w3c", False)
        driver_path = r"D:\msedgedriver.exe"
        super().__init__(executable_path=driver_path)
        self.wait = WebDriverWait(self, timeout=4, poll_frequency=1)
        self.wait2 = WebDriverWait(self, timeout=4, poll_frequency=1)
    
    def __del__(self):
        self.quit()

    def open(self, headless=True):
        # options = webdriver.EdgeOptions()
        # if headless:
        #     options.add_argument('--headless')
        # super().__init__()
        pass
    
    def landFirstPage(self):
        self.get(const.BASE_URL)
    
    def search(self,drug_name):
        element = self.find_element(By.ID, 'livesearch-main')
        element.clear()
        element.send_keys(drug_name,Keys.ENTER)
    
    def back(self):
        script= "return window.history.back()"
        self.execute_script(script)
    
    def closePopUp(self,clas='ddc-modal-close'):
        try:
            element = self.wait2.until(EC.element_to_be_clickable((By.CLASS_NAME, clas)))
            element.click()
        except:
            print('not here')
    
    def closeSmallPopUp(self):
        try:
            element = self.wait2.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='fc-close']'=")))
            element.click()
            print('closed')
        except:
            print('not here')
    
    def hashing(self,txt):
        hash=0
        for i in range(len(txt)):
            hash = (hash+ord(txt[i]) * 13** (len(txt)-i-1) ) % 1000000031
        return hash