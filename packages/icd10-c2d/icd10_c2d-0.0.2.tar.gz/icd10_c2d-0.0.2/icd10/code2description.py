from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import requests

class Code2Description:
        def init():
                return 0

        def getICDDescription(icd,hideInvalid=False):
                parent = "https://www.icd10data.com/"
                code2desc = {}
                for code in icd:
                        page = requests.get(str(parent)+'search?s='+code)
                        soup = BeautifulSoup(page.content, 'html.parser')
                        for x in soup.find_all('a',href=True):
                                if(x['href'].startswith('ICD10CM')):
                                        actual_page = requests.get(parent+str(x['href']))
                                        soup = BeautifulSoup(actual_page.content,'html.parser')
                                        try:
                                                icddescription = soup.select_one('.codeDescription').get_text()
                                        except:
                                                icddescription = "Invalid ICD-10 Code"
                                                if hideInvalid==False:
                                                        code2desc[code]=icddescription
                                        code2desc[code]=icddescription
                                        break
                return code2desc
