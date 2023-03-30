from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

#Définition de la classe Scrapping permettant de récupérer le contenue d'une page
# à partir d'un URL en utilisant chrome

class Scrapping(): 
    def __init__(self, url):
        self.__url = url
    
#Méthode html_scrapping : méthode principal de Scrapping    
    def html_scrapping(self) -> webdriver:
        service = Service(executable_path=ChromeDriverManager().install())
        
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_experimental_option("detach", True) # permet de garder la fenêtre chrome ouverte pour voir ce qu'on fait
        options.add_experimental_option("excludeSwitches", ['enable-logging'])
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(self.__url)
        time.sleep(2) #Attente de 2sec pour que les animations de la page soient terminé
        
        return driver