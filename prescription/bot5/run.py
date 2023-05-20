
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


    def get_drugs_names(self):
        self.drug_obj.parent.landFirstPage(const.drugs_URL)
        return self.drug_obj.get_name_and_active_ingredient()
    

    def prepare_drugs(self,drugs=None):
        if drugs == None:
            drugs = self.get_drugs_names()
            
        for drug in drugs:
            try:
                self.drug_obj.SetDrug(drug)
                self.drug_obj.parent.landFirstPage()
                # self.drug_obj.parent.closePopUp()
                self.drug_obj.parent.search(drug)
                self.drug_obj.parent.closeSmallPopUp()
                self.drug_obj.interaction.click_interaction()
                self.drug_obj.parent.closeSmallPopUp()
                self.drug_obj.interaction.click_on_interaction_number()
                print(self.drug_obj.is_ingredient_has_1(self.drug_obj.interaction.ingredient))
                if self.drug_obj.is_ingredient_has_1(self.drug_obj.interaction.ingredient) == False:
                    self.drug_obj.interaction.run_add_drug_interaction_to_db()
            

                self.drug_obj.parent.search(drug)
                self.drug_obj.description.clickFirstLink()
                self.drug_obj.description.clickSideEffectLink()
                self.drug_obj.description.get_side_effects()
                self.drug_obj.description.drug_uses()
                self.drug_obj.description.drug_warnings()
                self.drug_obj.description.drug_overdose()
                self.drug_obj.description.drug_missed_dose()
                self.drug_obj.description.drug_how_to_take()
                self.drug_obj.description.drug_what_to_avoid()
                self.drug_obj.description.drug_before_taking()
                
                self.drug_obj.add_drug_to_db()
            except:
                continue



# run = RUN()
# run.prepare_drugs(['Femara'])



