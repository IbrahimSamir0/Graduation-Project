from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .D_B import DB

from .parent import PARENT
import time



class INTERACTION(PARENT):

    # def __init__(self):
    #     self.con= DB()

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    # functions for get drugs interactoin
    # ++++++++++++++++++++++++++++++++++++

    def click_interaction(self):
        try:
            link = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='content']/div[@class='contentBox']/div[@class='ddc-media-list ddc-search-results']/div[@class='ddc-media']/div[@class='ddc-media-content ddc-search-result ddc-search-result-with-secondary']/ul/li[3]/a")))
            link.click()
        except:
            return 'Cant git this drug!'

    def get_interaction_drugs(self):
        link = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="content"]/div[2]/ul[1]/li[1]/a')))
        link.click()

    def getIntSource(self, clas):
        return self.find_elements(By.XPATH, f"//h3[text()[contains(.,'disease')]]/preceding::ul/li[@class='{clas}']/a")[1:]

    def getIntText(self, clas):
        text = []
        for i in self.getIntSource(clas):
            text.append(i.text)
        return text

    def getIntLinks(self, clas):
        links = []
        for i in self.getIntSource(clas):
            links.append(i.get_attribute("href"))
        return links

    def validDescription(self, txt):
        if txt[:8] == 'Consumer' or txt[:6] == 'Switch' or txt[:11] == 'Information':
            return False
        return True
    
    
    def get_header(self):
        header = self.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/div/h3")
        return header
    
    def get_interaction(self):
        p = self.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/p")
        return p
    
    def validate_header(self,header,ingredient):
        txt= header.strip().split(' ')
        if ingredient not in txt:
            return [False]
        else:
            txt = ' '.join(txt)
            txt= txt.replace(ingredient,'').strip()
            return [True,txt]

    def validate_interaction(self,interactions,parent):
        ans=''
        for i in interactions:
            if i.parent == parent:
                interaction= i.text
                if interaction[:8] != 'Consumer' or interaction[:6] != 'Switch' or interaction[:11] != 'Information':
                    ans+='      '+interaction
        return ans
    
    def prepare_data(self,ingredient):
        header = self.get_header()
        interactions = self.get_interaction()
        res= {}
        for h,i in zip(header,interactions):
            res_h= self.validate_header(h.text,ingredient)
            if not res_h[0]:
                continue
            second_ingredient= res_h[1]
            description= self.validate_interaction(interactions,h.parent)
            res[second_ingredient]=description.strip()
        return res

    def getInteractionDescription(self):
        p = self.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/p")
        res=[]
        
        blocks=[]
        prev=p[0].parent
        
        for i in p:
            current= i.parent
            if current == prev:
                if self.validDescription(i.text):
                    blocks.append(i.text)
                else:
                    blocks.append(' ')
            else:
                res.append(blocks)
        if len(blocks):
            res.append(blocks)
        return res

    def getInteractWith(self, drug):
        #                                     //h3[contains(text(),'apremilast')]
        name = self.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/div/h3")
        
        res = {}
        counter=0
        for idx,i in enumerate(name):
            if idx==None:
                break
            ans = []
            txt = i.text
            if drug in txt:
                befor = len(txt)
                txt = txt.replace(drug, '')
                after = len(txt)
                if befor == after:
                    continue
                ans.append(txt.strip())
                description= self.getInteractionDescription()
                ans.append(description[counter%len(description)])
                
            if len(ans):
                counter+=1
        return res

    def active_ingredient(self,drug_name):
        first= self.find_elements(By.XPATH, '//*[@id="content"]/div[@class="contentBox"]/ul[1]/li')
        for i in first:
            res= i.text
            spl= res.split(' ')
            if spl[0].lower()==drug_name.lower():
                ingredient= spl[1]
                return ingredient[1:-1].lower()
    
    
    def get_name_of_active_ingredient(self,drug_name):
        links_2 = self.getIntLinks('int_2')
        self.get(links_2[0])
        res= self.active_ingredient(drug_name)
        self.back()
        return res


    # def run_user_add_active_ingredient(self,user_active_ingredients):
    #     # active_ingredient=set(user_active_ingredients)
    #     active = user_active_ingredients[0]
    #     data=[]
    #     db = DB()
    #     status=None
    #     db.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{active}'")
    #     print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        
    #     status = db.cursor.fetchall()[0]
    #     print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    #     # status = [i[0] for i in db.cursor.fetchall()[0]]
    #     # print(status)
    #     # status = status[0]
    #     if status == None:
    #         for i in user_active_ingredients:
    #             data.append((self.hashing(i),i,0))
    #         self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist ','%s,%s,%s',data)
    #     # elif status == 0 :
    #     #     self.con.raw(""" UPDATE `prescription_active_ingredient`
    #     #             SET `if_interaction_exist` = '%s'
    #     #             WHERE name = '%s'; """
    #     #         ,(1,active))
    
    
    

    def run_user_add_active_ingredient(self,active):
        status=None
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{active}'")
        status = self.con.cursor.fetchone()
        if status == None:
            self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.hashing(active),active,0))



    
    

    #----------------------------------------------add ingredients description-----------------------------------------------------[****************LAST WORK*******************]
    def run_go_to_description(self,ingredient_name):
        self.closePopUp()
        self.search(ingredient_name)
        self.closeSmallPopUp()
        self.click_interaction()
        self.closeSmallPopUp()
        self.get_interaction_drugs()
        self.closeSmallPopUp()
        
    
    def run_add_drug_interaction_to_db(self,ingredient):
        # self.closeSmallPopUp()
        self.find_element(By.XPATH, '//*[@id="content"]/div[2]/ul[1]/li[1]/a').click()
        links_3 = self.getIntLinks('int_3')
        links_2 = self.getIntLinks('int_2')
        links_1 = self.getIntLinks('int_1')
    # # Major
    #     for link in links_3[1:]:
    #         self.get(link)
    #         interact_with = self.prepare_data(ingredient)
    #         for name,description in interact_with.items():
    #             first= [(self.hashing(name),name,0)]
    #             self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist','%s,%s,%s',first)
    #             second= [(description,self.hashing(ingredient),self.hashing(name), 2)]
    #             self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id','%s,%s,%s,%s',second)
    # # Moderate
    #     for link in links_2:
    #         self.get(link)
    #         interact_with = self.prepare_data(ingredient)
    #         for name,description in interact_with.items():
    #             first= [(self.hashing(name),name,0)]
    #             self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist','%s,%s,%s',first)
    #             second= [(description,self.hashing(ingredient),self.hashing(name), 1)]
    #             self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id','%s,%s,%s,%s',second)
    # Minor
        for link in links_1[:3]:
            self.get(link)
            interact_with = self.prepare_data(ingredient)
            for name,description in interact_with.items():
                first= (self.hashing(name),name,0)
                self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',first)
                second= (description,self.hashing(ingredient),self.hashing(name), 0)
                self.con.insert('prescription_ingredient_interaction','description,first_id,second_id,status_id',second)

    #------------------------------------------------------------------------------------------------------------------



# interaction= INTERACTION()
# interaction.ingredient='toremifene'
# interaction.closePopUp()
# interaction.landFirstPage()
# interaction.closePopUp()
# interaction.search('toremifene')
# interaction.closeSmallPopUp()
# interaction.click_interaction()
# interaction.closeSmallPopUp()
# interaction.get_interaction_drugs()
# links=interaction.getIntLinks('int_2')
# interaction.get(links[0])
# interaction.closeSmallPopUp()
# interaction.prepare_data()

# last run---------------------------------------------------------------------------
# run = INTERACTION()
# run.open()
# run.landFirstPage()
# run.closeSmallPopUp()
# for i in ['toremifene']:
#     run.run_go_to_description(i)
#     run.run_add_drug_interaction_to_db(i)