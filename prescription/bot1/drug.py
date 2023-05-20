
from .parent import PARENT
from .interaction import INTERACTION
from .description import DESCRIPTION



class DRUG():
    def __init__(self):
        self.parent = PARENT()
        self.parent.open()
        
        self.__drug = None
        self.description = DESCRIPTION()
        self.interaction = INTERACTION(self.parent)
    
    

    def SetDrug(self,drug):
        self.__drug = drug
    
    def GetDrug(self):
        return self.__drug


    # def get_db_ingredients(self):
    #     db_ingredients=[]
    #     self.db.cursor.execute('select name from prescription_active_ingredient where if_interaction_exist = 1;')
    #     db_ingredients = [i[0] for i in self.db.cursor.fetchall()]
    def is_ingredient_has_None(self,ingredient):
        status=None
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{ingredient}'")
        status = self.con.cursor.fetchone()
        if status == None:
            return True
        else:
            return False
        

    def __add_drug_ingredient_to_db(self):

        if self.is_ingredient_has_None(self.interaction.ingredient):
            self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(self.interaction.ingredient),self.interaction.ingredient,0))

    def __add_ingredient_and_interactions(self):
        
        for ingredient, description in self.interaction.major_interactions.items():
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(self.interaction.ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(ingredient),self.parent.hashing(ingredient), 2))
        
        for ingredient, description in self.interaction.moderate_interactions.items():
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(self.interaction.ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(ingredient),self.parent.hashing(ingredient), 1))

        for ingredient, description in self.interaction.minor_interactions.items():
            if self.is_ingredient_has_None(ingredient):
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.parent.hashing(self.interaction.ingredient),ingredient,0))
            self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',(description,self.parent.hashing(ingredient),self.parent.hashing(ingredient), 0))

    def __add_drug_description(self):
        self.con.insert('prescription_standarddrugs','id,name,activeIngredient_id,sideEffects,uses,warnings,before_taking,how_to_take,miss_dose,overdose,what_to_avoid',
                        (self.hashing(self.__drug), self.__drug, self.hashing(self.interaction.ingredient), self.description.side_effects, self.description.uses,self.description.warnings, self.description.before_taking,self.description.how_to_take, self.description.miss_dose,self.description.overdose,self.description.what_to_avoid))

    def add_drug_to_db(self):
        self.__add_drug_ingredient_to_db()
        self.__add_ingredient_and_interactions()
        self.__add_drug_description()
        
    