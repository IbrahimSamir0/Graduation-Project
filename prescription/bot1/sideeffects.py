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
    side_effects={}
    description = {}
    uses = {}
    warnings={}
    before_taking = {}
    how_to_take = {}
    miss_dose = {}
    overdose = {}
    what_to_avoid ={}


    def clickFirstLink(self):
        link = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/div/a')))
        link.click()

    def clickSideEffectLink(self):
        # self.implicitly_wait(1)
        # driver.find_elements(By.XPATH, '//*[@id="content"]/div[2]/nav/ul/li[4]/a')[0].click()
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/nav/ul/li[4]/a')))
        element.click()
    
    
    def get_side_effects(self,drug_name):
        print('['*200)
        print(drug_name)
        print(']'*200)
        uls= self.find_elements(By.XPATH,"//ul[preceding-sibling::h2[@id='side-effects'] and following-sibling::h2[@id]]/li")
        # print(uls)
        res=' '
        for i in uls:
            txt= i.text.replace(';','.')
            txt= txt.replace('\'',' i')
            res+='  '+txt
        print('['*200)
        print(drug_name)
        print(']'*200)
        self.side_effects[drug_name]= res.strip()
        print(self.side_effects)
    
    def drug_uses(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='uses']")
        
        if self.uses.get(drug_name):
            self.uses[drug_name]+=' '+h2.text
        else:
            self.uses[drug_name] =' '+h2.text
            
        uses_h2_list = self.find_elements(By.XPATH,"//h2[@id='uses'] / following-sibling::*")
        
        for elem in uses_h2_list:
            if elem.tag_name == 'h2':
                break
            self.uses[drug_name]+=' '+elem.text
        print(self.uses)


    def drug_warnings(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='warnings']")
        
        if self.warnings.get(drug_name):
            self.warnings[drug_name]+=' '+h2.text
        else:
            self.warnings[drug_name] =' '+h2.text
            
        warnings_h2_list = self.find_elements(By.XPATH,"//h2[@id='warnings'] / following-sibling::*")
        
        for elem in warnings_h2_list:
            if elem.tag_name == 'h2':
                break
            self.warnings[drug_name]+=' '+elem.text
        print(self.warnings)


    def drug_before_taking(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='before-taking']")
        
        if self.before_taking.get(drug_name):
            self.before_taking[drug_name]+=' '+h2.text
        else:
            self.before_taking[drug_name] =' '+h2.text
            
        before_taking_h2_list = self.find_elements(By.XPATH,"//h2[@id='before-taking'] / following-sibling::*")
        
        for elem in before_taking_h2_list:
            if elem.tag_name == 'h2':
                break
            self.before_taking[drug_name]+=' '+elem.text
        print(self.before_taking)


    def drug_how_to_take(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='dosage']")
        
        if self.how_to_take.get(drug_name):
            self.how_to_take[drug_name]+=' '+h2.text.replace('\'',' i')
        else:
            self.how_to_take[drug_name] =' '+h2.text.replace('\'',' i')
            
        how_to_take_h2_list = self.find_elements(By.XPATH,"//h2[@id='dosage'] / following-sibling::*")
        
        for elem in how_to_take_h2_list:
            if elem.tag_name == 'h2':
                break
            # txt= txt.replace('\'',' i')
            self.how_to_take[drug_name]+=' '+elem.text.replace('\'',' i')
        print(self.how_to_take)
    

    def drug_missed_dose(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='missed-dose']")
        
        if self.miss_dose.get(drug_name):
            self.miss_dose[drug_name]+=' '+h2.text
        else:
            self.miss_dose[drug_name] =' '+h2.text
            
        miss_dose_h2_list = self.find_elements(By.XPATH,"//h2[@id='missed-dose'] / following-sibling::*")
        
        for elem in miss_dose_h2_list:
            if elem.tag_name == 'h2':
                break
            self.miss_dose[drug_name]+=' '+elem.text
        print(self.miss_dose)

    def drug_overdose(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='overdose']")
        
        if self.overdose.get(drug_name):
            self.overdose[drug_name]+=' '+h2.text
        else:
            self.overdose[drug_name] =' '+h2.text
            
        overdose_h2_list = self.find_elements(By.XPATH,"//h2[@id='overdose'] / following-sibling::*")
        
        for elem in overdose_h2_list:
            if elem.tag_name == 'h2':
                break
            self.overdose[drug_name]+=' '+elem.text
        print(self.overdose)
    
    def drug_what_to_avoid(self,drug_name):
        # Find all h2 elements with id='uses'
        h2 =self.find_element(By.XPATH,"//h2[@id='what-to-avoid']")
        
        if self.what_to_avoid.get(drug_name):
            self.what_to_avoid[drug_name]+=' '+h2.text
        else:
            self.what_to_avoid[drug_name] =' '+h2.text
            
        what_to_avoid_h2_list = self.find_elements(By.XPATH,"//h2[@id='what-to-avoid'] / following-sibling::*")
        
        for elem in what_to_avoid_h2_list:
            if elem.tag_name == 'h2':
                break
            self.what_to_avoid[drug_name]+=' '+elem.text
        print(self.what_to_avoid)

    
    def get_description(self,drug_name):
        #  //h2[@id = 'uses']/following-sibling::*[preceding-sibling::h2[@id='side-effects']]
        dd = self.find_elements(By.XPATH,"//h2[@id = 'uses']/following-sibling::*[following-sibling::h2[@id='side-effects']]")
        for i in dd:
            # print(i.text)
            txt= i.text
            # txt= txt.replace('\'',' i')
            if self.description.get(drug_name):
                self.description[drug_name]+=(' '+txt)
            else:
                self.description[drug_name]= '  '+txt
        print(self.description)
        
        
    
    def run_add_side_effects_db(self):
        data = [(description,drug) for drug,description in self.side_effects.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `sideEffects` = '%s'
                                WHERE name = '%s'; """
                            ,i)
    
    def run_add_uses(self):
        data = [(description,drug) for drug,description in self.uses.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `uses` = '%s'
                                WHERE name = '%s'; """
                            ,i)
            
    def run_add_warnings(self):
        data = [(description,drug) for drug,description in self.warnings.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `warnings` = '%s'
                                WHERE name = '%s'; """
                            ,i)

    def run_add_before_taking(self):
        data = [(description,drug) for drug,description in self.before_taking.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `before_taking` = '%s'
                                WHERE name = '%s'; """
                            ,i)
    
    def run_add_how_to_take(self):
        data = [(description,drug) for drug,description in self.how_to_take.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `how_to_take` = '%s'
                                WHERE name = '%s'; """
                            ,i)

    def run_add_miss_dose(self):
        data = [(description,drug) for drug,description in self.miss_dose.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `miss_dose` = '%s'
                                WHERE name = '%s'; """
                            ,i)


    def run_add_overdose(self):
        data = [(description,drug) for drug,description in self.overdose.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `overdose` = '%s'
                                WHERE name = '%s'; """
                            ,i)

    def run_add_what_to_avoid(self):
        data = [(description,drug) for drug,description in self.what_to_avoid.items()]
        for i in data:
            self.con.raw(""" UPDATE `prescription_standarddrugs`
                                SET `what_to_avoid` = '%s'
                                WHERE name = '%s'; """
                            ,i)

# run= SIDEEFFECTS()
# # run.open()
# run.landFirstPage()
# for i in ['nexavar']:
#     run.search(i)
#     run.clickFirstLink()
#     run.clickSideEffectLink()
#     run.get_side_effects(i)
#     run.run_add_side_effects_db()