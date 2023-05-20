import constant as const
from selenium.webdriver.common.by import By


class STANDARD_DRUGS:
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
