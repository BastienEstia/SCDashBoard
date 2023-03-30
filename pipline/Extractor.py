import time
import Scrapping as scrp
import bs4 as bs
from selenium.webdriver.common.by import By

# It opens a browser, scrolls down to the bottom of the page, and then returns the html code of the
# page

class extractor:
    
    def __init__(self, url, nb_tracks=None, date_cible=None):
        self.url = url
        self.nb_tracks = nb_tracks
        self.date_cible = date_cible
        
    def extracting_tag(self):
        return self.url.split("/")[-1]
    
    def extract(self):
            
            def fixdate(str):
                jour = str.split("T")[0]
                heure = str.split("T")[1].split(".")[0]
                datesql = f'{jour} {heure}'
                return datesql

            print("<<DEBUT EXTRACTION>>")

            print("Ouverture de Chrome...")
            browser = scrp.Scrapping(self.url).html_scrapping()

            #Appuiyer sur "accepter les cookies"
            print("Clic sur accepter cookies...")
            button_cookie_agree = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            button_cookie_agree.click()
            time.sleep(2)

            if self.date_cible:

                print("Première tracks trouvé !")
                data_item = bs.BeautifulSoup(browser.page_source, "html.parser")
                list_data_item = data_item.find_all("time", {"class": "relativeTime sc-text-secondary sc-text-captions"})
                item_datetime = fixdate(list_data_item[-1].get('datetime'))
                print(f"Date du premier item : {item_datetime}")

                while item_datetime>=self.date_cible:

                    browser.execute_script("window.scrollTo(0, 100000000)")
                    time.sleep(2)
                    data_item = bs.BeautifulSoup(browser.page_source, "html.parser")
                    list_data_item=data_item.find_all("time", {"class": "relativeTime sc-text-secondary sc-text-captions"})
                    item_datetime = fixdate(list_data_item[-1].get('datetime'))
                    
                    print(f"Date de l'item : {item_datetime}")
                    print("Scroll/")
                    
                print("Extraction du code source de la page...")
                data=data_item
                
            else:

                print("Première tracks trouvé !")
                list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")

                #Scroll down pour faire apparaitre plus d'item SC
                while len(list_data_item)<=self.nb_tracks:

                    browser.execute_script("window.scrollTo(0, 10000)")
                    time.sleep(2)
                    list_data_item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                    print("Scroll/")
                
                print("Extraction du code source de la page...")   
                data = bs.BeautifulSoup(browser.page_source, "html.parser")

            print(f"Nombre de tracks repéré : {len(list_data_item)}")

            print("Fermeture de Chrome...")
            browser.quit() 

            print("<<FIN EXTRACTION>>")

            return data