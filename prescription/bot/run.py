


from . drug import DRUG
from . import constant as const
from . standard_drugs import STANDARD_DRUGS

class RUN():
    # db = DB()
    
    

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
        standard_drugs = STANDARD_DRUGS()
        standard_drugs.parent.landFirstPage(const.drugs_URL)
        return standard_drugs.get_name_and_active_ingredient()
    

    def prepare_drugs(self,drugs=None):
        print('entered')
        if drugs == None:
            drugs = self.get_drugs_names()
        
        ln = len(drugs)
        i =276
        for drug in drugs[i:]:
            drug_obj = DRUG()
            print(drug)
            print('-'*100)
            print(f'drug {i} from {ln} drugs')
            print('-'*50)
            print('h1')
        # try:
            drug_obj.SetDrug(drug)
            drug_obj.parent.landFirstPage(const.BASE_URL)
            print('h1')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.parent.search(drug)
            print('h2')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.interaction.click_interaction()
            print('h3')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.interaction.click_on_interaction_number()
            print('h4')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            if not drug_obj.is_ingredient_has_1(drug_obj.interaction.ingredient):
                drug_obj.interaction.scrapInteractions()
                print('f1')
        
            if not drug_obj.interaction.ingredient:
                continue
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.parent.search(drug)
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.description.clickFirstLink()
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.description.clickSideEffectLink()
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.description.get_side_effects()
            drug_obj.description.drug_uses()
            drug_obj.description.drug_warnings()
            drug_obj.description.drug_overdose()
            drug_obj.description.drug_missed_dose()
            drug_obj.description.drug_how_to_take()
            drug_obj.description.drug_what_to_avoid()
            drug_obj.description.drug_before_taking()
            
            drug_obj.add_drug_to_db()
            print(f'drug number {i} ended')
            print('#'*150)
            i += 1



run = RUN()
run.prepare_drugs()

