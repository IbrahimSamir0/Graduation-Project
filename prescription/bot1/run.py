from .sideeffects import SIDEEFFECTS
from .interaction import INTERACTION
from .drugs1 import DRUG
from .D_B import DB
from .sideeffects import SIDEEFFECTS
from .parent import PARENT

# con= DB()
# drug = Drugs()

# # drug.DrugsForNonSmallCell()
# DRUG= drug.DrugsForNonSmallCell()


# SQL= ("INSERT INTO prescription_standarddrugs (name) VALUES (%s)")
# SQL= ('SELECT `name` FROM `prescription_standarddrugs` ;')
# res= con.cursor.execute(SQL)
# print(res)

# # print(tuple(DRUG))
# for i in DRUG:
#     con.raw(SQL,([i]))


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
        # self.close()
        return res

    # def go_to_side_effects(self,drug_name):
        
    #     self.search(drug_name)
    #     # self.closePopUp()
    #     self.clickFirstLink()
    #     # self.closeSmallPopUp()
    
    
    def prepare_drugs(self,drugs=None):
        # first fill drugs data in DRUG CLASS
        if drugs==None:
            self.land_first_page()
            self.get_name_and_active_ingredient()
            # self.run_add_drugs_db()
        else:
            for drug in drugs:
                self.data[drug]= self.get_active_ingredient_for_user_drug(drug)
                print('jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj')
                print(self.data[drug])
        db = DB()
        db_ingredients = db.select('name','prescription_active_ingredient')
        ingredients = [i for i in self.data.values() if i not in db_ingredients]
        
        for ingredient in ingredients:
            try:
                self.run_user_add_active_ingredient([ingredient])
                self.run_add_drug_interaction_to_db(ingredient)
            except:
                print('ingredient already in db')
            
        self.landFirstPage()
        print(';'*100)
        print(self.data)
        print(';'*100)
        
        for drug in self.data.keys():
            # try:
                self.search(drug)
                self.closePopUp()
                self.clickFirstLink()
                self.closeSmallPopUp()
                self.clickSideEffectLink()
                print('~'*200)
                print(drug)
                print('~'*200)
                self.get_side_effects(drug)
                print('description \n')
                self.drug_uses(drug)
                self.drug_warnings(drug)
                self.drug_overdose(drug)
                self.drug_missed_dose(drug)
                self.drug_how_to_take(drug)
                self.drug_what_to_avoid(drug)
                self.drug_before_taking(drug)
                # self.back()
            # except:
            #     print('33333333333333333333333333333333333333333333333333333333333333333333333333333333333')
            
        
        
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
        
#----------------------------------------------------------------------------------------------------------------------
    
#---------------------------------------------ingredients block--------------------------------------------------------
#
#there are two cases for adding ingredients
#
#                                   /                           \
#                       get ingredients from website            doctor added drug but his ingredient not in database so
#                                                                       \
#                                                                       get ingredient name   ------> get interaction


    # def prepare_ingredients(self,):



#----------------------------------------------------------------------------------------------------------------------


    
    # def run_add_active_ingredient(self):
    #     if self.standard_drugs==None:
    #         self.get_standerd_drugs()
    #     active_ingredient=set(self.standard_drugs.values())
    #     data=[]
    #     for i in active_ingredient:
    #         data.append((self.hashing(i),i))
    #     self.con.insert('prescription_interaction','ID,name','%s,%s',data)
    







    #------------------------------------------------got to series-----------------------------------------------------  
    #------------------------------------------------------------------------------------------------------------------


    # def add_interaction_to_db(self):

    #     self.landFirstPage()
    #     for i in self.new_drugs:
    #         print('&'*1000)
    #         self.search(i)
    #         print(i)
    #         self.closeSmallPopUp()
    #         self.click_interaction()
    #         self.closePopUp()
    #         self.get_interaction_drugs()
    #         self.closePopUp()

    #         self.getDrugInteraction(i)
    #         self.closePopUp()




# interacion = INTERACTION()
# interacion.landFirstPage()
# interacion.search('cocaine')








# run = RUN()
# run.run_user_add_drugs(['Cosentyx'])
# run.run_user_add_active_ingredient(['haha'])
# run.run_user_add_drugs(['medo'])
# run.run_add_drugs()




# run= RUN()
# run.run_add_active_ingredient()

# interacion = INTERACTION()


# run = RUN()
# run.open()
# run.prepare_drugs(['Afinitor'])


# run = RUN()
# run.open()
# run.landFirstPage()
# run.closeSmallPopUp()
# for i in ['toremifene']:
#     run.run_go_to_description(i)
#     run.run_add_drug_interaction_to_db(i)








# side= SIDEEFFECTS()
# drug= DRUG()
# side.landFirstPage()
# side.search('Otezla')
# side.clickFirstLink()
# drug.land_first_page()



# with SIDEEFFECTS() as bot:

#     bot.landFirstPage()
#     for i in ['Otezla']:
#         bot.search(i)
#         print(i)
#         bot.clickFirstLink()
#         bot.closeSmallPopUp()
#         bot.clickSideEffectLink()
#         print(i)
#         bot.getSideEffects()
#         bot.back()
#         bot.closeSmallPopUp()
#         bot.back()
#         # bot.closePopUp()
#         bot.closeSmallPopUp()
#         print('111111111111111')


# # alecensa have problem
# with INTERACTION() as bot:

#     bot.landFirstPage()
#     for i in ['Otezla']:
#         print('&'*1000)
#         bot.search(i)
#         print(i)
#         bot.closeSmallPopUp()
#         bot.click_interaction()
#         bot.closePopUp()
#         bot.get_interaction_drugs()
#         bot.closePopUp()

#         bot.getDrugInteraction(i)
#         bot.closePopUp()



