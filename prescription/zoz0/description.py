# import constant as const
# from selenium.webdriver.support import expected_conditions as EC
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from selenium.webdriver.edge import service
# import time
# from selenium.webdriver.support.wait import WebDriverWait
from .parent import PARENT




class DESCRIPTION():
    def __init__(self,parent):
        self.parent = parent
        self.driver = self.parent.driver
        
        self.drug_name=None
        self.side_effects=None
        self.uses = None
        self.warnings=None
        self.before_taking = None
        self.how_to_take = None
        self.miss_dose = None
        self.overdose = None
        self.what_to_avoid = None



    def clickFirstLink(self):
        try:
            link =self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/div/a')
            link.click()
        except Exception as e:
            return str(e)

    def clickSideEffectLink(self):
        try:
            element = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/nav/ul/li[4]/a')
            element.click()
        except Exception as error:
            print(error)
    
    def text_validation(self,txt):
        txt= txt.replace(';','.')
        txt= txt.replace('\'',' i')
        return txt
    
    def get_side_effects(self):
        uls= self.driver.find_elements(By.XPATH,"//ul[preceding-sibling::h2[@id='side-effects'] and following-sibling::h2[@id]]/li")
        res=' '
        for i in uls:
            txt= i.text
            txt= self.text_validation(txt)
            res+='  '+txt
        self.side_effects= res.strip()
        # print(self.side_effects)
    
    def drug_uses(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='uses']")
    
        self.uses =' '+h2.text
            
        uses_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='uses'] / following-sibling::*")
        
        for elem in uses_h2_list:
            
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.uses +=' '+txt


    def drug_warnings(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='warnings']")
        
        self.warnings =' '+h2.text
            
        warnings_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='warnings'] / following-sibling::*")
        
        for elem in warnings_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.warnings+=' '+txt


    def drug_before_taking(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='before-taking']")
        self.before_taking =' '+h2.text
            
        before_taking_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='before-taking'] / following-sibling::*")
        
        for elem in before_taking_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.before_taking+=' '+txt


    def drug_how_to_take(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='dosage']")
        
        self.how_to_take =' '+h2.text.replace('\'',' i')
            
        how_to_take_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='dosage'] / following-sibling::*")
        
        for elem in how_to_take_h2_list:
            if elem.tag_name == 'h2':
                break
            # txt= txt.replace('\'',' i')
            txt= self.text_validation(elem.text)
            self.how_to_take+=' '+txt
    

    def drug_missed_dose(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='missed-dose']")
        
        self.miss_dose =' '+h2.text
            
        miss_dose_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='missed-dose'] / following-sibling::*")
        
        for elem in miss_dose_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.miss_dose+=' '+txt

    def drug_overdose(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='overdose']")
        

        self.overdose =' '+h2.text
            
        overdose_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='overdose'] / following-sibling::*")
        
        for elem in overdose_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.overdose+=' '+txt
    
    def drug_what_to_avoid(self):
        # Find all h2 elements with id='uses'
        h2 =self.driver.find_element(By.XPATH,"//h2[@id='what-to-avoid']")
        

        self.what_to_avoid =' '+h2.text
            
        what_to_avoid_h2_list = self.driver.find_elements(By.XPATH,"//h2[@id='what-to-avoid'] / following-sibling::*")
        
        for elem in what_to_avoid_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.what_to_avoid+=' '+txt
        
        


# run= SIDEEFFECTS()
# # run.open()
# run.landFirstPage()
# for i in ['nexavar']:
#     run.search(i)
#     run.clickFirstLink()
#     run.clickSideEffectLink()
#     run.get_side_effects(i)
#     run.run_add_side_effects_db()