

from . drug import DRUG
from . import constant as const
from . standard_drugs import STANDARD_DRUGS
import traceback

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
    

    def prepare_drugs(self, drugs=None):
        print('entered')
        
        if drugs == None:
            drugs = self.get_drugs_names()
            
        # ln = len(drugs)
        # i = 1
        problem_drug = set()
        
        for drug in drugs:
            prob = 1
            drug_obj = DRUG()
            print('-'*100)
            print(drug)
            print('-'*100)
            # print(f'drug {i} from {ln} drugs')
            # print('-'*50)
            print('h1')

            drug_obj.SetDrug(drug)
            drug_obj.parent.landFirstPage(const.BASE_URL)
            print('h1')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            drug_obj.parent.search(drug)
            print('h2')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            prob = drug_obj.interaction.click_interaction()
            if prob == 0:
                problem_drug.add(drug)
            print(prob)
            print('h3')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()
            prob = drug_obj.interaction.click_on_interaction_number()
            if prob == 0:
                problem_drug.add(drug)
            print('h4')
            drug_obj.parent.closeSmallPopUp()
            drug_obj.parent.closePopUp()

            if not drug_obj.is_ingredient_has_1(drug_obj.interaction.ingredient):
                prob = drug_obj.interaction.scrapInteractions()
                if prob == 0:
                    problem_drug.add(drug)
                print('f1')
        
            if drug_obj.interaction.ingredient:
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
                

            
            # print(f'drug number {i} ended')
            print('#'*150)
                
            # i += 1
        
        # print(list(problem_drug))
        return list(problem_drug)



# run = RUN()
# run.prepare_drugs(['afinitor'])



