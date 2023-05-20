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
from .parent import PARENT
# import pysnooper




class DRUG(PARENT):

    data={}

    def land_first_page(self):
        self.get(const.drugs_URL)
    
    def split_name_from_active_ingredient(self,txt):
        drug,active_ingredient= txt.split('(')[:2]
        active_ingredient = active_ingredient.split('-')[0]
        active_ingredient= active_ingredient.split(' ')[0]
        if active_ingredient[-1] ==')':
            active_ingredient = active_ingredient[:-1]
        return [drug.strip(), active_ingredient.strip()]
    


    def validate_active_ingredient_in_data(self):
        res=set()
        for i in self.data.values():
            if len(i)>=3:
                res.add(i.lower())
        self.data = {k:v for k,v in self.data.items() if v.lower() in res}

    def get_name_and_active_ingredient(self):
        res= self.find_elements(By.XPATH,"//ul[@class='drugs-list']/li/h4/a")
        for i in res:
            name, active_ingredient= self.split_name_from_active_ingredient(i.text)
            self.data[name.lower()]=active_ingredient.lower()

    
    
    def get_data(self):
        if not len(self.data) :
            self.get_name_and_active_ingredient()
        return self.data


    #----------------------------add standard drugs---------------------------------------------------------------------
    def run_add_drugs_db(self):
        flow=[]
        for drug,ingredient in self.data.items():
            flow.append((self.hashing(drug),drug,self.hashing(ingredient)))
        self.con.insert('prescription_standarddrugs','id,name,activeIngredient_id','%s,%s,%s',flow)
    #------------------------------------------------------------------------------------------------------------------
