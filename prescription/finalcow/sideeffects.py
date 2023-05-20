from . import constant as const
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
# from selenium.webdriver.edge import service
import time
from selenium.webdriver.support.wait import WebDriverWait
from .parent import PARENT



class SIDEEFFECTS(PARENT):
    drug_name=None
    side_effects=None
    uses = None
    warnings=None
    before_taking = None
    how_to_take = None
    miss_dose = None
    overdose = None
    what_to_avoid =None


    def clickFirstLink(self):
        try:
            link = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/div/a')))
            link.click()
        except Exception as e:
            return str(e)

    def clickSideEffectLink(self):
        # self.implicitly_wait(1)
        # driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/nav/ul/li[4]/a')[0].click()
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/nav/ul/li[4]/a')))
        element.click()
    def text_validation(self,txt):
        txt= txt.replace(';','.')
        txt= txt.replace('\'',' i')
        return txt
    
    def get_side_effects(self,drug_name):
        print('['*200)
        print(drug_name)
        print(']'*200)
        uls= self.find_elements(By.XPATH,"//ul[preceding-sibling::h2[@id='side-effects'] and following-sibling::h2[@id]]/li")
        # print(uls)
        res=' '
        for i in uls:
            txt= i.text
            txt= self.text_validation(txt)
            res+='  '+txt
        print('['*200)
        print(drug_name)
        print(']'*200)
        self.side_effects= res.strip()
        print(self.side_effects)
    
    def drug_uses(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='uses']")
    
        self.uses =' '+h2.text
            
        uses_h2_list = self.find_elements(By.XPATH,"//h2[@id='uses'] / following-sibling::*")
        
        for elem in uses_h2_list:
            
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.uses +=' '+txt


    def drug_warnings(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='warnings']")
        
        self.warnings =' '+h2.text
            
        warnings_h2_list = self.find_elements(By.XPATH,"//h2[@id='warnings'] / following-sibling::*")
        
        for elem in warnings_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.warnings+=' '+txt


    def drug_before_taking(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='before-taking']")
        self.before_taking =' '+h2.text
            
        before_taking_h2_list = self.find_elements(By.XPATH,"//h2[@id='before-taking'] / following-sibling::*")
        
        for elem in before_taking_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.before_taking+=' '+txt


    def drug_how_to_take(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='dosage']")
        
        self.how_to_take =' '+h2.text.replace('\'',' i')
            
        how_to_take_h2_list = self.find_elements(By.XPATH,"//h2[@id='dosage'] / following-sibling::*")
        
        for elem in how_to_take_h2_list:
            if elem.tag_name == 'h2':
                break
            # txt= txt.replace('\'',' i')
            txt= self.text_validation(elem.text)
            self.how_to_take+=' '+txt
    

    def drug_missed_dose(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='missed-dose']")
        
        self.miss_dose =' '+h2.text
            
        miss_dose_h2_list = self.find_elements(By.XPATH,"//h2[@id='missed-dose'] / following-sibling::*")
        
        for elem in miss_dose_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.miss_dose+=' '+txt

    def drug_overdose(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='overdose']")
        

        self.overdose =' '+h2.text
            
        overdose_h2_list = self.find_elements(By.XPATH,"//h2[@id='overdose'] / following-sibling::*")
        
        for elem in overdose_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.overdose+=' '+txt
    
    def drug_what_to_avoid(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='what-to-avoid']")
        

        self.what_to_avoid =' '+h2.text
            
        what_to_avoid_h2_list = self.find_elements(By.XPATH,"//h2[@id='what-to-avoid'] / following-sibling::*")
        
        for elem in what_to_avoid_h2_list:
            if elem.tag_name == 'h2':
                break
            txt= self.text_validation(elem.text)
            self.what_to_avoid+=' '+txt

    
    # def get_description(self,drug_name):
    #     #  //h2[@id = 'uses']/following-sibling::*[preceding-sibling::h2[@id='side-effects']]
    #     dd = self.find_elements(By.XPATH,"//h2[@id = 'uses']/following-sibling::*[following-sibling::h2[@id='side-effects']]")
    #     for i in dd:
    #         # print(i.text)
    #         txt= i.text
    #         # txt= txt.replace('\'',' i')
    #         if self.description.get(drug_name):
    #             self.description[drug_name]+=(' '+txt)
    #         else:
                
    #             self.description[drug_name]= '  '+txt
    #     print(self.description)
        
        
    
    def run_add_side_effects_db(self):
        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `sideEffects` = '%s'
                            WHERE name = '%s'; """
                        ,(self.side_effects,self.drug_name))

    
    def run_add_uses(self):
        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `uses` = '%s'
                            WHERE name = '%s'; """
                        ,(self.uses,self.drug_name))

    def run_add_warnings(self):

        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `warnings` = '%s'
                            WHERE name = '%s'; """
                        ,(self.warnings,self.drug_name))


    def run_add_before_taking(self):
        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `before_taking` = '%s'
                            WHERE name = '%s'; """
                        ,(self.before_taking,self.drug_name))

    
    def run_add_how_to_take(self):

        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `how_to_take` = '%s'
                            WHERE name = '%s'; """
                        ,(self.how_to_take,self.drug_name))


    def run_add_miss_dose(self):

        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `miss_dose` = '%s'
                            WHERE name = '%s'; """
                        ,(self.miss_dose,self.drug_name))



    def run_add_overdose(self):

        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `overdose` = '%s'
                            WHERE name = '%s'; """
                        ,(self.overdose,self.drug_name))


    def run_add_what_to_avoid(self):
        self.con.raw(""" UPDATE `prescription_standarddrugs`
                            SET `what_to_avoid` = '%s'
                            WHERE name = '%s'; """
                        ,(self.what_to_avoid,self.drug_name))
    
    
    def SET_DRUG(self,name):
        self.drug_name =name


# run= SIDEEFFECTS()
# # run.open()
# run.landFirstPage()
# for i in ['nexavar']:
#     run.search(i)
#     run.clickFirstLink()
#     run.clickSideEffectLink()
#     run.get_side_effects(i)
#     run.run_add_side_effects_db()