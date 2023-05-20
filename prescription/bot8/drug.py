
from .parent import PARENT
from .interaction import INTERACTION
from .description import DESCRIPTION
from .D_B import DB
from selenium.webdriver.common.by import By


class DRUG():
    def __init__(self):
        self.parent = PARENT()
        self.parent.open()
        self.con= DB()
        self.driver = self.parent.driver
        
        self.__drug = None
        self.description = DESCRIPTION()
        self.interaction = INTERACTION(self.parent)
        self.drugs_names = []
    
    

    def SetDrug(self,drug):
        self.__drug = drug
    
    def GetDrug(self):
        return self.__drug


    def is_ingredient_has_None(self,ingredient):
        status=None
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{ingredient}'")
        status = self.con.cursor.fetchone()
        if status :
            status = status[0]
            
        if status == None:
            return True
        else:
            return False
    def is_ingredient_has_0(self,ingredient):
        status=None
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{ingredient}' and if_interaction_exist = 0")
        status = self.con.cursor.fetchone()
        if status :
            status = status[0]
        if status == 0:
            return True
        else:
            return False
    
    def is_ingredient_has_1(self,ingredient):
        status=None
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{ingredient}' and if_interaction_exist = 1")
        status = self.con.cursor.fetchone()
        if status :
            status = status[0]
            
        print('*'*20)
        print(status)
        print('*'*20)
        if status == 1:
            return True
        else:
            return False

    def __add_drug_ingredient_to_db(self):

        if self.is_ingredient_has_None(self.interaction.ingredient):
            self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(self.interaction.ingredient),self.interaction.ingredient,1))
        elif self.is_ingredient_has_0(self.interaction.active_ingredient):
            self.con.raw(""" UPDATE `prescription_active_ingredient`SET `if_interaction_exist` = '%s'WHERE name = '%s'; """,(1,self.interaction.ingredient))
            

    def __add_ingredient_and_interactions(self):
        
        for ingredient, description in self.interaction.major_interactions:
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(self.interaction.ingredient),self.parent.hashing(ingredient), 2))
        
        for ingredient, description in self.interaction.moderate_interactions:
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(self.interaction.ingredient),self.parent.hashing(ingredient), 1))

        for ingredient, description in self.interaction.minor_interactions:
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(self.interaction.ingredient),self.parent.hashing(ingredient), 0))

    def __add_drug_description(self):
        self.con.insert('prescription_standarddrugs','id,name,activeIngredient_id,sideEffects,uses,warnings,before_taking,how_to_take,miss_dose,overdose,what_to_avoid',
                        (self.parent.hashing(self.__drug), self.__drug, self.parent.hashing(self.interaction.ingredient), self.description.side_effects, self.description.uses,self.description.warnings, self.description.before_taking,self.description.how_to_take, self.description.miss_dose,self.description.overdose,self.description.what_to_avoid))

    def add_drug_to_db(self):
        self.__add_drug_ingredient_to_db()
        self.__add_ingredient_and_interactions()
        self.__add_drug_description()
    
    
    
    
    
    
    
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
        
    


