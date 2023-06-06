

from . import constant as const
from . parent import PARENT
from selenium.webdriver.common.by import By

class STANDARD_DRUGS:
    
    def __init__(self):
        self.parent = PARENT()
        self.driver = self.parent.driver
        self.drugs_names = []
        
        
    
    
    def split_name_from_active_ingredient(self,txt):
        drug,active_ingredient= txt.split('(')[:2]
        active_ingredient = active_ingredient.split('-')[0]
        active_ingredient= active_ingredient.split(' ')[0]
        if active_ingredient[-1] ==')':
            active_ingredient = active_ingredient[:-1]
        return [drug.strip(), active_ingredient.strip()]
    

    def get_name_and_active_ingredient(self):
        res= self.driver.find_elements(By.XPATH,"//ul[@class='drugs-list']/li/h4/a")
        for i in res:
            name, _= self.split_name_from_active_ingredient(i.text)
            self.drugs_names.append(name.lower())
        return self.drugs_names
