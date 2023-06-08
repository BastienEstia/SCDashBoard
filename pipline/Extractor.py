import time
import Scraping as scrp
import bs4 as bs
import json 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pipline.Transformer import transformer as t
import logging as l
import sys 
import gc
from datetime import datetime

logger = l.getLogger("Extractor")
logger.setLevel(l.DEBUG)
formatter = l.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = l.StreamHandler(sys.stdout)
stdout_handler.setLevel(l.INFO)
stdout_handler.setFormatter(formatter)

fh = l.FileHandler("/home/devadmin/Pythons_Scripts/MS_DB/SCDashBoard/pipline/logs/Extractor.log", "w")
fh.mode = 'w'
fh.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(fh)



# It opens a browser, scrolls down to the bottom of the page, and then returns the html code of the
# page

class extractor:
    
    def __init__(self, url, mode=None, nb_tracks=None,date_depart = None, date_cible=None):
        self.url = url
        if mode:
            self.mode = mode
        else:
            self.mode = "d" 
        self.nb_tracks = nb_tracks
        self.date_depart = date_depart
        self.date_cible = date_cible
              
    
    def extracting_tag(self):
        return self.url.split("/")[-1]
    
    @staticmethod
    def reversedate(str):
        logger.debug(f"str : {str}")
        date=str.split(' ')[0]
        heure = str.split(' ')[1]
        return f'{date}T{heure}.000Z' 

    """
    @staticmethod
    def fixdate(str):
        jour = str.split("T")[0]
        heure = str.split("T")[1].split(".")[0]
        return f'{jour} {heure}'
    """
    def extractByWebPageSourceCode(self, scrollingSpeed = None):  # sourcery skip: replace-interpolation-with-fstring

            def tryFindByCSSElement(browser, value):
                try:
                    browser.find_element(By.XPATH,"//time[contains(@datetime,'%s')]" %value)
                    return 1
                except NoSuchElementException:
                    return -1
                    

            logger.info("<<DEBUT EXTRACTION>>")

            logger.info("Ouverture de Chrome...")
            browser = scrp.Scraping(self.url).html_scraping()

            #Appuiyer sur "accepter les cookies"
            logger.info("Clic sur accepter cookies...")
            button_cookie_agree = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            button_cookie_agree.click()
            browser.implicitly_wait(1)
            tag = extractor.extracting_tag(self)
            
            if self.date_cible:
                
                while tryFindByCSSElement(browser,self.date_cible) == -1:
                    
                    browser.execute_script("window.scrollTo(0, 100000000)")
                    logger.info("Scroll/")
                    browser.implicitly_wait(0.1)
                    if scrollingSpeed:
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        logger.info("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        logger.info("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        logger.info("Scroll/")
                        browser.implicitly_wait(1)
                        browser.execute_script("window.scrollTo(0, 100000000)")
                        logger.info("BigScroll/")
                        browser.implicitly_wait(1)
                    
                data = bs.BeautifulSoup(browser.page_source, "html.parser")
            else:
                
                list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                logger.info("Première tracks trouvé !")
                
                #Scroll down pour faire apparaitre plus d'item SC
                while len(list_data_item)<=self.nb_tracks:

                    browser.execute_script("window.scrollTo(0, 10000)")
                    time.sleep(2)
                    list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                    logger.info("Scroll/")
                
                logger.info("Extraction du code source de la page...")   
                data = bs.BeautifulSoup(browser.page_source, "html.parser")

            logger.info("Fermeture de Chrome...")
            browser.quit() 

            logger.info("<<FIN EXTRACTION>>")

            return data
        
    def extractByAPI(self):
        
        @staticmethod        
        def reqConstructor(date):
            return f"https://api-v2.soundcloud.com/recent-tracks/{self.extracting_tag()}?offset={extractor.reversedate(date)}%2Crecent-content-tracks-by-tag%2Csoundcloud%3Atracks%3A1482398899&limit=10&client_id=tyFGpYeFlJG938Pu0R4ibFdtNBkvBkcJ&app_version=1685711325&app_locale=fr"
        
        @staticmethod
        def buildDataList(item, datalist):
            datalist.append(item)
            return data
        
        @staticmethod
        def writeToFile(item):
            with open(f"/home/devadmin/Pythons_Scripts/MS_DB/SCDashBoard/tmp/{datetime.now().date()}-Extraction-{self.date_depart}-{self.date_cible}.json", "a") as f:
                json.dump(item, f)
        
        @staticmethod
        def writeToMultipleFiles(datalist):
            with open(f"/home/devadmin/Pythons_Scripts/MS_DB/SCDashBoard/tmp/{datetime.now().date()}-Extraction-{self.date_depart}-{self.date_cible}-file_{i}.json", "a") as f:
                json.dump(datalist, f)
        
        n = 0
        i = 0
        # if self.mode=="d":
        data = []
        dataw = {}               
        procReq = None
        logger.info("<<DEBUT EXTRACTION>>")

        logger.info("Ouverture de Chrome...")
        browser = scrp.Scraping().API_scraping()
        while True:
            i = i + 1
            
            logger.debug(f"request to SC : {procReq or reqConstructor(self.date_depart)}")
            browser.get(procReq or reqConstructor(self.date_depart))
            dataCollection = json.loads(bs.BeautifulSoup(browser.page_source, "html.parser").get_text())
            procReq = f"{dataCollection['next_href']}&client_id=tyFGpYeFlJG938Pu0R4ibFdtNBkvBkcJ&app_version=1685711325&app_locale=fr"
            logger.info(f"Requête : {i} ---------------------------------------------------------------------------------------")
            
            match self.mode:
                case "d":
                    for item in dataCollection["collection"]:
                        logger.debug(f"item_type : {type(item)}")
                        logger.debug(f"item_print : {item}")
                        buildDataList(item, data)
                        n = n + 1
                        logger.info(f"Item : {n} | created_at : {t.fixdate(item['created_at'])}")
                        logger.debug(f"nb objets en RAM : {gc.get_count()}")
                case "wd":
                    for item in dataCollection["collection"]:
                        writeToFile(item)
                        buildDataList(item, data)
                        n = n + 1
                        logger.info(f"Item : {n} | created_at : {t.fixdate(item['created_at'])}")
                        logger.debug(f"nb objets en RAM : {gc.get_count()}")
                case "wmf":
                    for item in dataCollection["collection"]:
                        n = n + 1
                        logger.info(f"Item : {n} | created_at : {t.fixdate(item['created_at'])}")
                        logger.debug(f"nb objets en RAM : {gc.get_count()}")
                    writeToMultipleFiles(dataCollection)
                    
                case "wmfd":
                    for item in dataCollection["collection"]:
                        
                        buildDataList(item, data) 
                        # buildDataList(item, dataw)
                        n = n + 1
                        logger.info(f"Item : {n} | created_at : {t.fixdate(item['created_at'])}")
                        logger.debug(f"nb objets en RAM : {gc.get_count()}")
                        
                    # writeToMultipleFiles(dataw)
                    # dataw.clear()
                    writeToMultipleFiles(dataCollection)
                    
            # END CONDITION :       
            try:
            
                if t.fixdate(dataCollection["collection"][-1]["created_at"])<=self.date_cible:
                    break
        
            except IndexError as error:
                logger.error(error)
                continue
            
        logger.info("")
        logger.info("Fermeture de Chrome...")    
        browser.quit()
        logger.info("<<FIN EXTRACTION>>")
        logger.info("")
        
        match self.mode:
            case "d":
                return data
            case "wd":
                return data
            case "wmfd":
                return data
            case "wmf":
                pass