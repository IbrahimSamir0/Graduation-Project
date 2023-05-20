from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .parent import PARENT
import time
from selenium.webdriver.support.ui import WebDriverWait


class INTERACTION():
    def __init__(self,parent = PARENT()):
        self.parent = parent
        self.driver = self.parent.driver
        
        self.ingredient = None
        self.major_interactions = {}
        self.minor_interactions = {}
        self.moderate_interactions ={}

    def click_interaction(self):
        try:
            link = self.driver.find_element(By.XPATH, '//*[@class="ddc-list-column-2"]/li[3]/a')
            url = str(link.get_attribute("href"))
            url = url.split(',')[0]
            self.ingredient = url.split('/')[-1]
            print(self.ingredient)
            link.click()
        except:
            return 'Can\'t get this drug!'
    # click_on_interaction_number______________________________________________________________________________________________________________________________________
    def click_on_interaction_number(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/ul[1]/li[1]/a').click()
        except Exception as error:
            print(error)
            

    def getIntSource(self, clas):
        return self.driver.find_elements(By.XPATH, f"//h3[text()[contains(.,'disease')]]/preceding::ul/li[@class='{clas}']/a")[1:]


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
        header = self.driver.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/div/h3")
        return header

    def get_interaction(self):
        p = self.driver.find_elements(
            By.XPATH, f"//div[@class='interactions-reference']/p")
        return p

    def validate_header(self,header):
        txt= header.strip().split(' ')
        if self.ingredient not in txt:
            return [False]
        else:
            txt = ' '.join(txt)
            txt= txt.replace(self.ingredient,'').strip()
            return [True,txt]


    def validate_interaction(self,interactions,parent):
        ans=''
        for i in interactions:
            if i.parent == parent:
                interaction= i.text
                if interaction[:8] != 'Consumer' or interaction[:6] != 'Switch' or interaction[:11] != 'Information':
                    ans+='      '+interaction
        return ans

    def prepare_data(self):
        header = self.get_header()
        interactions = self.get_interaction()
        res= {}
        for h,i in zip(header,interactions):
            res_h= self.validate_header(h.text)
            if not res_h[0]:
                continue
            second_ingredient= res_h[1]
            description= self.validate_interaction(interactions,h.parent)
            res[second_ingredient]=description.strip()
        return res


    def getInteractionDescription(self):
        p = self.driver.find_elements(
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
        name = self.driver.find_elements(
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
        first= self.driver.find_elements(By.XPATH, '//*[@id="content"]/div[@class="contentBox"]/ul[1]/li')
        for i in first:
            res= i.text
            spl= res.split(' ')
            if spl[0].lower()==drug_name.lower():
                ingredient= spl[1]
                return ingredient[1:-1].lower()


    def get_name_of_active_ingredient(self,drug_name):
        links_2 = self.getIntLinks('int_2')
        self.driver.get(links_2[0])
        res= self.active_ingredient(drug_name)
        self.back()
        return res


    def run_user_add_active_ingredient(self,active):
        status=None
        self.con.cursor.execute(f"SELECT if_interaction_exist FROM prescription_active_ingredient WHERE name = '{active}'")
        status = self.con.cursor.fetchone()
        if status == None:
            self.con.insert('prescription_active_ingredient','id,name,if_interaction_exist',(self.hashing(active),active,0))

















    #----------------------------------------------add ingredients description-----------------------------------------------------[****************LAST WORK*******************]
    def run_go_to_description(self,drug):
        # self.parent.closePopUp()
        self.search(drug)
        # self.parent.closeSmallPopUp()
        self.click_interaction()
        # self.parent.closeSmallPopUp()
        self.click_on_interaction_number()
        # self.parent.closeSmallPopUp()
        
    
    def run_add_drug_interaction_to_db(self):
        # self.parent.closeSmallPopUp()
        # self.parent.closePopUp()
        # self.click_on_interaction_number()
        # self.parent.closeSmallPopUp()
        links_3 = self.getIntLinks('int_3')
        links_2 = self.getIntLinks('int_2')
        links_1 = self.getIntLinks('int_1')
        c=0
    # Major
        for link in links_3[1:]:
            self.driver.get(link)
            self.parent.closeSmallPopUp()
            self.major_interactions = self.prepare_data()
            c+=1
            print(c)

    # # Moderate
    #     for link in links_2:
    #         self.driver.get(link)
    #         self.parent.closeSmallPopUp()
    #         self.moderate_interactions = self.prepare_data()
    #         c+=1
    #         print(c)

    # # Minor
    #     for link in links_1:
    #         self.driver.get(link)
    #         self.parent.closeSmallPopUp()
    #         self.minor_interactions = self.prepare_data()
    #         c+=1
    #         print(c)


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
# interaction.click_on_interaction_number()
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