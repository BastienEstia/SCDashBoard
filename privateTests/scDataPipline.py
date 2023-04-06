import bs4 as bs
from selenium.webdriver.common.by import By
import time
import Scrapping as scrp
import Connect as co
#response = rq.get(url) gardé pour test api

# 1- Effectuer un scrapping avec les parametre voulue
# 2- Transformé les données en tuple 
# 3- Load les données dans la base PostgreSQL

#DEBUT PROGRAMME PRINCIPAL


# The class is a pipeline that takes a url, a number of tracks and a date as input and returns a list
# of dictionaries containing the data of the tracks
class pipline():
    
    def __init__(self) -> None:
        pass
    
    def extract(url, nb_tracks=None, date_cible=None):
        
        def fixdate(str):
            jour = str.split("T")[0]
            heure = str.split("T")[1].split(".")[0]
            datesql = f'{jour} {heure}'
            return datesql

        print("<<DEBUT EXTRACTION>>")

        print("Ouverture de Chrome...")
        browser = scrp.Scrapping(url).html_scrapping()

        #Appuiyer sur "accepter les cookies"
        print("Clic sur accepter cookies...")
        button_cookie_agree = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
        button_cookie_agree.click()
        time.sleep(2)

        if date_cible:

            print("Première tracks trouvé !")
            item = browser.find_elements(By.CLASS_NAME, "soundList__item")
            data_item = bs.BeautifulSoup(item[len(item)-1]._parent.page_source, "html.parser")
            item_datetime = fixdate(data_item.find("time", {"class": "relativeTime sc-text-secondary sc-text-captions"}).get('datetime'))
            print(f"Date du premier item : {item_datetime}")

            while item_datetime>=date_cible:

                browser.execute_script("window.scrollTo(0, 100000000)")
                time.sleep(2)
                item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                data_item = bs.BeautifulSoup(browser.page_source, "html.parser")
                list_data_item=data_item.find_all("time", {"class": "relativeTime sc-text-secondary sc-text-captions"})
                item_datetime = fixdate(list_data_item[-1].get('datetime'))
                print(f"Date de l'item : {item_datetime}")
                print("Scroll/")
        else:

            print("Première tracks trouvé !")
            item = browser.find_elements(By.CLASS_NAME, "soundList__item")

            #Scroll down pour faire apparaitre plus d'item SC
            while len(item)<=nb_tracks:

                browser.execute_script("window.scrollTo(0, 10000)")
                time.sleep(2)
                item = browser.find_elements(By.CLASS_NAME, "soundList__item")
                print("Scroll/")

        print(f"Nombre de tracks repéré : {len(item)}")

        print("Extraction du code source de la page...")
        data=bs.BeautifulSoup(browser.page_source, "html.parser")

        print("Fermeture de Chrome...")
        browser.quit() 

        print("<<FIN EXTRACTION>>")

        return data       
        
    def transform(data):
        
        def fixstr(str):
            return str.replace("'","''")

        def fixdate(str):
            jour = str.split("T")[0]
            heure = str.split("T")[1].split(".")[0]
            datesql = f'{jour} {heure}'
            return datesql

        def fixinteger(str):
            try:
                strlist = str.split(".")
                new_int = int(''.join(strlist))
            except(ValueError):
                strlist = str.split(",")
                new_int = int(''.join(strlist))
            return new_int

        print("")
        print("<<DEBUT TRANSFORMATION>>")

        print("Récupération des items contnenant les données...")
        tracks = data.find_all("li", {"class": "soundList__item"})

        print("Transformation des données... ")
        print("")
        datas = []
        for track in tracks:

            d_data = {
                "artist": fixstr(track.find("span", {"class": "soundTitle__usernameText"}).get_text(strip=True)),
                "date": fixdate(track.find("time", {"class": "relativeTime sc-text-secondary sc-text-captions"}).get('datetime')),
                }
            try:
                d_data["title"] = fixstr(track.find("a", {"class": "sc-link-primary soundTitle__title sc-link-dark sc-text-h4"}).findChildren()[0].get_text(strip=True))
            except(AttributeError):
                d_data["title"] = fixstr(track.find("a", {"class": "sc-link-primary soundTitle__title g-opacity-transition-500 g-type-shrinkwrap-block g-type-shrinkwrap-primary theme-dark sc-text-h4"}).findChildren()[0].get_text(strip=True))

            try:
                d_data["num_likes"] = fixinteger(track.find("button", {"class": "sc-button-like sc-button-secondary sc-button sc-button-small sc-button-responsive"}).get_text())
            except(ValueError):
                d_data["num_likes"] = 0

            if track.find("a", {"class": "sc-ministats sc-ministats-small sc-ministats-comments sc-link-secondary"}):
                d_data["num_comments"] = fixinteger(track.find("a", {"class": "sc-ministats sc-ministats-small sc-ministats-comments sc-link-secondary"}).findChildren()[1].get_text())
            else:
                d_data["num_comments"] = 0

            if track.find("span", {"class": "sc-ministats sc-ministats-small sc-ministats-plays sc-text-secondary"}):
                d_data["num_streams"] = fixinteger(track.find("span", {"class": "sc-ministats sc-ministats-small sc-ministats-plays sc-text-secondary"}).findChildren()[1].get_text())
            else:
                d_data["num_streams"] = 0

            if track.find("span", {"class": "sc-truncate sc-tagContent"}):
                d_data["main_tag"] = fixstr(track.find("span", {"class": "sc-truncate sc-tagContent"}).get_text())
            else:
                d_data["main_tag"] = "Null"

            if track.find("a", {"class": "sc-ministats sc-ministats-small sc-link-secondary sc-text-h4 sc-ministats-followers "}):
                d_data["num_abonnes"] = fixinteger(track.find("a", {"class": "sc-ministats sc-ministats-small sc-link-secondary sc-text-h4 sc-ministats-followers "}).findChildren()[1].get_text())
            else:
                d_data["num_abonnes"] = 0

            print("Nouvelle ligne :")
            print(d_data)
            print("")

            """
            print("titre : " + str(d_data["title"]) + "\n" +
            "artist : " + str(d_data["artist"]) + "\n" +
            "date : " + str(d_data["date"]) + "\n" +
            "num_likes : " + str(d_data["num_likes"]) + "\n" +
            "num_comments : " + str(d_data["num_comments"]) + "\n" +
            "num_streams : " + str(d_data["num_streams"]) + "\n" +
            "main_tag : " + str(d_data["main_tag"]))
            """

            datas.append(d_data)

        print("<<FIN EXTRACTION>>")

        return datas

    def load(self) -> None:
        print("")
        print("<<DEBUT LOADING>>")

        conn = co.connect.connection()
        print('Connexion à la base de données établie !')

        cur = conn.cursor()

        print("DEBUT REQUÊTES INSERTION")
        for i in range(len(self)):
            
            try:
                #Requête d'insertion table artiste
                sql_artists = (
                    "INSERT INTO public.artists(artist_name, num_sub) VALUES ('%s','%d') ON CONFLICT DO NOTHING;"
                    % (self[i]["artist"], self[i]["num_abonnes"])
                )
                cur.execute(sql_artists)
                print("")
                print("Requête %d artiste : %s" %(i,sql_artists))

            except UnicodeEncodeError as error:
                
                print(f"Probleme enconding data dans la requête : {error.args[1]}")
                #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                self[i]["artist"] = "Null"
                sql_artists = (
                    "INSERT INTO public.artists(artist_name, num_sub) VALUES ('%s',%d) ON CONFLICT DO NOTHING;"
                    % (self[i]["artist"], self[i]["num_abonnes"])
                )
                cur.execute(sql_artists)
                print("Requête %d artiste avec null : %s" %(i,sql_artists))

            try:    
                #Requête d'insertion table tags
                sql_tags = f"""INSERT INTO public.tags(tag_name) VALUES ('{self[i]["main_tag"]}') ON CONFLICT DO NOTHING;"""
                cur.execute(sql_tags)
                print("Requête %d tag : %s" %(i,sql_tags))

            except UnicodeEncodeError as error:
                
                print(f"Probleme enconding data dans la requête : {error.args[1]}")
                #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                self[i]["main_tag"] = "Null"
                sql_tags = f"""INSERT INTO public.tags(tag_name) VALUES ('{self[i]["main_tag"]}') ON CONFLICT DO NOTHING;"""
                cur.execute(sql_tags)
                print("Requête %d tag avec Null : %s" %(i,sql_tags))

            try:        
                #Requête d'insertion table tracks
                sql_tracks = (
                    "INSERT INTO public.tracks(title, artists_id, datep, num_likes, num_comments, num_streams, maintag) VALUES ('%s',(SELECT artists_id FROM artists WHERE artist_name = '%s'),'%s','%d','%d','%d',(SELECT tags_id FROM tags WHERE tag_name = '%s')) ON CONFLICT (title) DO UPDATE SET num_likes = %d, num_comments = %d, num_streams = %d WHERE tracks.title = '%s';"
                    % (
                        self[i]["title"],
                        self[i]["artist"],
                        self[i]["date"],
                        self[i]["num_likes"],
                        self[i]["num_comments"],
                        self[i]["num_streams"],
                        self[i]["main_tag"],
                        self[i]["num_likes"],
                        self[i]["num_comments"],
                        self[i]["num_streams"],
                        self[i]["title"],
                    )
                )
                cur.execute(sql_tracks)
                print("Requête %d track : %s" %(i,sql_tracks))

            except UnicodeEncodeError as error:
                
                print(f"Probleme enconding data dans la requête : {error.args[1]}")
                #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                self[i]["title"] = "Null"
                sql_tracks = (
                    "INSERT INTO public.tracks(title, artists_id, datep, num_likes, num_comments, num_streams, maintag) VALUES ('%s',(SELECT artists_id FROM artists WHERE artist_name = '%s'),'%s','%d','%d','%d',(SELECT tags_id FROM tags WHERE tag_name = '%s')) ON CONFLICT DO NOTHING;"
                    % (
                        'Null',
                        self[i]["artist"],
                        self[i]["date"],
                        self[i]["num_likes"],
                        self[i]["num_comments"],
                        self[i]["num_streams"],
                        self[i]["main_tag"],
                    )
                )
                cur.execute(sql_tracks)
                print("Requête %d track avec null : %s" %(i,sql_tracks))

            conn.commit()
            print("")
            print("Commit éffectué pour les 3 dernières requêtes !")

        print("")
        print("Fin des requête d'insertion")

        cur.close()
        print("Curseur fermé")
        conn.close()
        print("Connexion avec la base de données fermée")
        print("<<FIN LOADING>>")      
        

