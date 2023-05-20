from . sideeffects import SIDEEFFECTS
from . interaction import INTERACTION
from . drugs1 import DRUG
from . D_B import DB
from . sideeffects import SIDEEFFECTS


class RUN(INTERACTION,DRUG,SIDEEFFECTS):
    db = DB()

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
    
    def run_standard_list(self):
        db_ingredients=[]
        self.db.cursor.execute('select name from prescription_active_ingredient where if_interaction_exist = 1;')
        db_ingredients = [i[0] for i in self.db.cursor.fetchall()]
        self.land_first_page()
        self.get_name_and_active_ingredient()
        self.landFirstPage()
        del self.data['abitrexate']
        # del self.data['abraxane']
        for drug , ingredient in self.data.items():
            self.SET_DRUG(drug)
            if ingredient not in db_ingredients:
                try:
                    self.closeSmallPopUp()
                    self.search(drug)
                    self.closePopUp()
                    self.click_interaction()
                    self.closeSmallPopUp()
                    print('hhhhh')
                    self.run_user_add_active_ingredient(ingredient)
                    print('ccccc')
                    self.run_add_drug_interaction_to_db(ingredient)
                    self.db.raw(""" UPDATE `prescription_active_ingredient`
                        SET `if_interaction_exist` = '%s'
                        WHERE name = '%s'; """
                    ,(1,ingredient))
                except:
                    print('ingredient already in db')
                
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
            self.run_add_drugs_db(drug)
            self.run_add_side_effects_db()
            self.run_add_uses()
            self.run_add_warnings()
            self.run_add_before_taking()
            self.run_add_how_to_take()
            self.run_add_miss_dose()
            self.run_add_what_to_avoid()
            self.run_add_overdose()
        

    def prepare_drugs(self,drugs):
        db_ingredients=[]
        self.db.cursor.execute('select name from prescription_active_ingredient where if_interaction_exist = 1;')
        db_ingredients = [i[0] for i in self.db.cursor.fetchall()]
        # first fill drugs data in DRUG CLASS

        for drug in drugs:
            try:
                active_ingredient = self.get_active_ingredient_for_user_drug(drug)
                self.data[drug]= active_ingredient
            except:
                print(f'cant get get active ingredient for this drug {drug}')

        for drug , ingredient in self.data.items():
            self.SET_DRUG(drug)
            if ingredient not in db_ingredients:
                try:
                    self.closeSmallPopUp()
                    self.search(drug)
                    self.closePopUp()
                    self.click_interaction()
                    self.closeSmallPopUp()
                    print('hhhhh')
                    self.run_user_add_active_ingredient(ingredient)
                    print('ccccc')
                    self.run_add_drug_interaction_to_db(ingredient)
                    self.db.raw(""" UPDATE `prescription_active_ingredient`
                        SET `if_interaction_exist` = '%s'
                        WHERE name = '%s'; """
                    ,(1,ingredient))
                except:
                    print('ingredient already in db')
                
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
            self.run_add_drugs_db(drug)
            self.run_add_side_effects_db()
            self.run_add_uses()
            self.run_add_warnings()
            self.run_add_before_taking()
            self.run_add_how_to_take()
            self.run_add_miss_dose()
            self.run_add_what_to_avoid()
            self.run_add_overdose()
        


run = RUN()
run.open()
# run.prepare_drugs(['Kyleena'])
run.run_standard_list()



