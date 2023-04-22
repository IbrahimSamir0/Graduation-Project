import requests
from . import constant as const
from bs4 import BeautifulSoup


class Drugs():
    def __init__(self):
        self.page = requests.get(const.NHI_URL)
        self.html = self.page.content   
        self.soup = BeautifulSoup(self.html,'html.parser')
        self.NonSmallCell = set()
        self.SmallCell = set()
    
    def DrugsForNonSmallCell(self):
        NonSmallCell_ui = self.soup.find(id ='1')
        for i in NonSmallCell_ui.find_all('a'):
            drugs = i.text.split('(')
            for j in drugs:
                j = j.split('\xa0')[0]
                if ')' in j:
                    j = j[:-1]
                j = j.strip().lower()
                self.NonSmallCell.add(max(j.split('-')))
                
            # drug = i.text.split('(')[0].strip().lower()
            # if len(drug) >=3:
            #     self.NonSmallCell.append(drug)
        # remove not needed data
        self.NonSmallCell.remove('everolimus)\n\tafinitor disperz')
        self.NonSmallCell.remove('')
        #-------------------------
        return list(self.NonSmallCell)
    
    def DrgsForSmallCell(self):
        SmallCell_ui = self.soup.find(id ='3')
        
        for i in SmallCell_ui.find_all('a'):
            drug = i.text.split('(')[0].strip().lower()
            if len(drug) >=3:
                self.SmallCell.add(drug)
        # remove not needed data
        self.SmallCell.remove('methotrexate\xa0sodium')
        #-------------------------
        return self.SmallCell