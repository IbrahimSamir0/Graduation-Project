from .sideeffects import SIDEEFFECTS
from .interaction import INTERACTION
from .drugs1 import DRUG
from .D_B import DB
from .sideeffects import SIDEEFFECTS


class RUN(INTERACTION,DRUG,SIDEEFFECTS):

#-------------------------------------drugs block--------------------------------------------------------------------
#
#                                                   there are two cases for adding drugs 
#                       /                                                                                   \
# get drugs from website in constant                                                                  get drugs from user
#                   |                                                                                         |
#      active ingredient in db?                                                                  get his active ingredient
#         /             \                                                                                    |
# save drug       get ingredient interaction with other ingredients                              active ingredient in db? 
#                        \                                                                                /            \
#                   save drug                                                                       save drug        get ingredient interaction with other ingredients
#                                                                                                                            |
#                                                                                                                        save drug
#
    def get_active_ingredient_for_user_drug(self,drug_name):
        self.landFirstPage()
        self.closeSmallPopUp()
        self.search(drug_name)
        self.closePopUp()
        self.click_interaction()
        self.closeSmallPopUp()
        res= self.get_name_of_active_ingredient(drug_name)
        return res

    def prepare_drugs(self,drugs=None):
        # first fill drugs data in DRUG CLASS
        err_list=[]
        if drugs==None:
            self.land_first_page()
            self.get_name_and_active_ingredient()
        else:
            for drug in drugs:
                try:
                    active_ingredient = self.get_active_ingredient_for_user_drug(drug)
                    self.data[drug]= active_ingredient
                except:
                    print(f'cant get get active ingredient for this drug {drug}')
                    err_list.append(drug)
                    
                
        print(self.data)
        # check if ingredient in db or not
        db = DB()
        db_ingredients = db.select('name','prescription_active_ingredient')
        ingredients = [i for i in self.data.values() if i not in db_ingredients] # get active ingredient not in db
        
        for ingredient in ingredients:
            try:
                self.run_user_add_active_ingredient([ingredient])
                self.run_add_drug_interaction_to_db(ingredient)
            except:
                print('ingredient already in db')
            
        self.landFirstPage()
        
        for drug in self.data.keys():
            try:
                self.search(drug)
                self.closePopUp()
                error= self.clickFirstLink()
                if error is not None:
                    print(f"An error occurred while clicking the first link for {drug}: {error}")
                    continue
                self.closeSmallPopUp()
                self.clickSideEffectLink()
                self.get_side_effects(drug)
                self.drug_uses(drug)
                self.drug_warnings(drug)
                self.drug_overdose(drug)
                self.drug_missed_dose(drug)
                self.drug_how_to_take(drug)
                self.drug_what_to_avoid(drug)
                self.drug_before_taking(drug)
            except Exception as e:
                print(f"An error occurred while processing {drug}: {e}")
            
        
        
        # second add collected data in database
        self.run_add_drugs_db()
        self.run_add_side_effects_db()
        self.run_add_uses()
        self.run_add_warnings()
        self.run_add_before_taking()
        self.run_add_how_to_take()
        self.run_add_miss_dose()
        self.run_add_what_to_avoid()
        self.run_add_overdose()
                
        return err_list
        


# run = RUN()
# run.open()
# run.prepare_drugs(['Entresto'])



