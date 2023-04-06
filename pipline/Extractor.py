import time
import Scraping as scrp
import bs4 as bs
import json 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# It opens a browser, scrolls down to the bottom of the page, and then returns the html code of the
# page

class extractor:
    
    def __init__(self, url, nb_tracks=None,date_depart = None, date_cible=None):
        self.url = url
        self.nb_tracks = nb_tracks
        self.date_depart = date_depart
        self.date_cible = date_cible
    
    def extracting_tag(self):
        return self.url.split("/")[-1]
    
    @staticmethod
    def reversedate(str):
                date=str.split(' ')[0]
                heure = str.split(' ')[1]
                return f'{date}T{heure}.000Z' 


    @staticmethod
    def fixdate(str):
        jour = str.split("T")[0]
        heure = str.split("T")[1].split(".")[0]
        datesql = f'{jour} {heure}'
        return datesql
    
    def extractByWebPageSourceCode(self, scrollingSpeed = None):  # sourcery skip: replace-interpolation-with-fstring
            
            """ 
            """
            
            def tryFindByCSSElement(browser, value):
                try:
                    browser.find_element(By.XPATH,"//time[contains(@datetime,'%s')]" %value)
                    return 1
                except NoSuchElementException:
                    return -1
                    

            print("<<DEBUT EXTRACTION>>")

            print("Ouverture de Chrome...")
            browser = scrp.Scraping(self.url).html_scraping()

            #Appuiyer sur "accepter les cookies"
            print("Clic sur accepter cookies...")
            button_cookie_agree = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            button_cookie_agree.click()
            browser.implicitly_wait(1)
            tag = extractor.extracting_tag(self)
            
            if self.date_cible:
                
                while tryFindByCSSElement(browser,self.date_cible) == -1:
                    
                    browser.execute_script("window.scrollTo(0, 100000000)")
                    print("Scroll/")
                    browser.implicitly_wait(0.1)
                    if scrollingSpeed:
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        print("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        print("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        print("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        print("BigScroll/")
                        browser.implicitly_wait(1)
                    
                data = bs.BeautifulSoup(browser.page_source, "html.parser")
            else:
                
                list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                print("Première tracks trouvé !")
                
                #Scroll down pour faire apparaitre plus d'item SC
                while len(list_data_item)<=self.nb_tracks:

                    browser.execute_script("window.scrollTo(0, 10000)")
                    time.sleep(2)
                    list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                    print("Scroll/")
                
                print("Extraction du code source de la page...")   
                data = bs.BeautifulSoup(browser.page_source, "html.parser")

            print("Fermeture de Chrome...")
            browser.quit() 

            print("<<FIN EXTRACTION>>")

            return data
        
    def extractByAPI(self):
        
        @staticmethod        
        def reqConstructor(date):
            return f"https://api-v2.soundcloud.com/recent-tracks/{self.extracting_tag()}?offset={extractor.reversedate(date)}%2Crecent-content-tracks-by-tag%2Csoundcloud%3Atracks%3A1482398899&limit=10&client_id=RMDIzNoU4QIzQsT3xq9J5TdxFFQlJvLY&app_version=1679652891&app_locale=fr"

        n = 0
        i = 0
        data = []
        procReq = None
        print("<<DEBUT EXTRACTION>>")

        print("Ouverture de Chrome...")
        browser = scrp.Scraping().API_scraping()
        while True:
            i = i + 1
            browser.get(procReq or reqConstructor(self.date_depart))
            dataCollection = json.loads(bs.BeautifulSoup(browser.page_source, "html.parser").get_text())
            procReq = f"{dataCollection['next_href']}&client_id=RMDIzNoU4QIzQsT3xq9J5TdxFFQlJvLY&app_version=1679652891&app_locale=fr"
            print(f"Requête : {i} ---------------------------------------------------------------------------------------")
            for item in dataCollection["collection"]:
                data.append(item)
                n = n + 1
                print(f"Item : {n}\n created_at : {item['created_at']}")
            try:
            
                if extractor.fixdate(dataCollection["collection"][-1]["created_at"])<=self.date_cible:
                    break
        
            except IndexError as error:
                print(error)
                continue
            
        print("")
        print("Fermeture de Chrome...")    
        browser.quit()
        print("<<FIN EXTRACTION>>")
        print("")
        
        return data