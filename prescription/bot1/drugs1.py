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




class DRUG(PARENT):
    # def __init__(self):
    #     self.open()
        # super(DRUG, self).__init__()
    data={}
        # self.active_ingredient= []
        
    
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
        # self.validate_active_ingredient_in_data()

    
    
    def get_data(self):
        if not len(self.data) :
            self.get_name_and_active_ingredient()
        return self.data




    #----------------------------add standard drugs---------------------------------------------------------------------
    def run_add_drugs_db(self):
        flow=[]
        for drug,ingredient in self.data.items():
            # print((i,self.hashing(self.standard_drugs[i])))
            flow.append((self.hashing(drug),drug,self.hashing(ingredient)))
        self.con.insert('prescription_standarddrugs','id,name,activeIngredient_id','%s,%s,%s',flow)
    #------------------------------------------------------------------------------------------------------------------






    


    #------------------------------------------------add new drug-----------------------------------------------------
    
    # first get active ingredient for this drug

    
    #get side effects for this drug
    
    
    # def run_user_add_drugs_db(self,user_drugs):
    #     drugs=set(user_drugs)
    #     # if active ingredient already saved
        
    #     data=[]
    #     for i in drugs:
    #         active_ingredient= self.get_active_ingredient_for_user_drug(i)
    #         print(f'active ingredient===================> {active_ingredient}')
    #         active_ingredient_data = (self.hashing(active_ingredient),active_ingredient)
    #         self.con.insert('prescription_interaction','ID,name','%s,%s',[active_ingredient_data])  # try to insert active ingredient if saved will prent already here else will add it
    #         # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!now we need add all data for this active ingredient!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
    #         data.append((i,self.hashing(active_ingredient)))
        
        
    #     self.con.insert('prescription_standarddrugs','name,active_ingredient','%s,%s',data)
    
    #------------------------------------------------------------------------------------------------------------------










# will move it to run
    def get_standerd_drugs(self):
        self.land_first_page()
        self.standard_drugs = self.get_data()
        # self.close()
    
    