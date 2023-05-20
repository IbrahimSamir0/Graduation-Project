
from .interaction import INTERACTION
from .drug import DRUG
from . import constant as const
import time



class RUN():
    # db = DB()
    drug_obj = DRUG()

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
        self.search(drug_name)
        self.click_interaction()
        res= self.get_name_of_active_ingredient(drug_name)
        return res
    
 
    def prepare_drugs(self,drugs):
        for drug in drugs:
            self.drug_obj.SetDrug(drug)
            print('hi1')
            self.drug_obj.parent.landFirstPage()
            print('hi1')
            self.drug_obj.parent.search(drug)
            self.drug_obj.parent.closeSmallPopUp()
            print('hi1')
            self.drug_obj.interaction.click_interaction()
            self.drug_obj.parent.closeSmallPopUp()
            print('hi1')
            self.drug_obj.interaction.run_add_drug_interaction_to_db()
            time.sleep(1)
            print('hi1')

            self.drug_obj.parent.search(drug)
            self.drug_obj.description.clickSideEffectLink()
            self.drug_obj.description.get_side_effects(drug)
            self.drug_obj.description.drug_uses(drug)
            self.drug_obj.description.drug_warnings(drug)
            self.drug_obj.description.drug_overdose(drug)
            self.drug_obj.description.drug_missed_dose(drug)
            self.drug_obj.description.drug_how_to_take(drug)
            self.drug_obj.description.drug_what_to_avoid(drug)
            self.drug_obj.description.drug_before_taking(drug)

            
            self.drug_obj.add_drug_to_db()



# run = RUN()
# run.prepare_drugs(['afinitor'])
# run.run_standard_list()
