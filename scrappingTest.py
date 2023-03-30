import requests as rq
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import Scrapping as scrp

#response = rq.get(url) gardé pour test api

#DEBUT PROGRAMME PRINCIPAL
URL="https://soundcloud.com/tags/acidcore"
ITEM_NB = 50

browser = scrp.Scrapping(URL).html_scrapping()

#Appuiyer sur "accepter les cookies"
button_cookie_agree = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
button_cookie_agree.click()
#browser.get(URL)
time.sleep(2)
items = browser.find_elements(By.CLASS_NAME, "soundList__item")
print("Première tracks trouvé !")

#Scroll down pour faire apparaitre plus d'item SC
while len(items)<=ITEM_NB:
    browser.execute_script("window.scrollTo(0, 10000)")
    time.sleep(2)
    items = browser.find_elements(By.CLASS_NAME, "soundList__item")
    print("Scroll/")

print(f"Nombre de tracks récupéré : {len(items)}")
soup=bs.BeautifulSoup(browser.page_source, "html.parser")
print("")
browser.quit()

for _ in items:
    track = soup.find_all("a", {"class": "sc-link-primary soundTitle__title sc-link-dark sc-text-h4"})
    print(track)

#print(items[0])
print(len(items))