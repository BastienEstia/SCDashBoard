import logging as l 

l.basicConfig(filename='SCDashBoard/pipline/logs/Transformer.log', filemode='w', format='%(asctime)s %(message)s', encoding='UTF-8', level=l.INFO)

# It's a class that transforms data
class transformer:
    
    def __init__(self):
        pass
    
    @staticmethod        
    def fixstr(str):
        return str.replace("'", "''") if str else "null"

    @staticmethod 
    def fixdate(date):
        if date :
            jour = date.split("T")[0]
            heure = date.split("T")[1].split(".")[0]
            return f'{jour} {heure}'
        else :
            return '0000-00-00 00:00:00'

    @staticmethod
    def fixinteger(value):
        # sourcery skip: last-if-guard, remove-redundant-slice-index, remove-unnecessary-else, simplify-negative-index, swap-if-else-branches
        if value:
            # determine multiplier
            if value.find(",") != -1:
                value = f"{value.split(',')[0]}.{value.split(',')[1]}"
            multiplier = 1
            if value.endswith('K'):
                multiplier = 1000
                value = value[0:len(value)-1] # strip multiplier character
            elif value.endswith('M'):
                multiplier = 1000000
                value = value[0:len(value)-1] # strip multiplier character

            return int(float(value) * multiplier)

        else:
            l.info(f'integer {value} = 0')
            return 0

    def transformPageSourceToRowData(data):
        # sourcery skip: extract-duplicate-method, instance-method-first-arg-name
        l.info("")
        l.info("<<DEBUT TRANSFORMATION>>")

        l.info("Récupération des items contnenant les données...")
        tracks = data.find_all("li", {"class": "soundList__item"})

        l.info("Transformation des données... ")
        l.info("")
        datas = []
        for track in tracks:

            d_data = {
                "artist": transformer.fixstr(track.find("span", {"class": "soundTitle__usernameText"}).get_text(strip=True)),
                "date": transformer.fixdate(track.find("time", {"class": "relativeTime sc-text-secondary sc-text-captions"}).get('datetime')),
                }
            try:
                d_data["title"] = transformer.fixstr(track.find("a", {"class": "sc-link-primary soundTitle__title sc-link-dark sc-text-h4"}).findChildren()[0].get_text(strip=True))
            except(AttributeError):
                d_data["title"] = transformer.fixstr(track.find("a", {"class": "sc-link-primary soundTitle__title g-opacity-transition-500 g-type-shrinkwrap-block g-type-shrinkwrap-primary theme-dark sc-text-h4"}).findChildren()[0].get_text(strip=True))

            try:
                d_data["num_likes"] = transformer.fixinteger(track.find("button", {"class": "sc-button-like sc-button-secondary sc-button sc-button-small sc-button-responsive"}).get_text())
            except(ValueError):
                d_data["num_likes"] = 0

            if track.find("a", {"class": "sc-ministats sc-ministats-small sc-ministats-comments sc-link-secondary"}):
                d_data["num_comments"] = transformer.fixinteger(track.find("a", {"class": "sc-ministats sc-ministats-small sc-ministats-comments sc-link-secondary"}).findChildren()[1].get_text())
            else:
                d_data["num_comments"] = 0

            if track.find("span", {"class": "sc-ministats sc-ministats-small sc-ministats-plays sc-text-secondary"}):
                d_data["num_streams"] = transformer.fixinteger(track.find("span", {"class": "sc-ministats sc-ministats-small sc-ministats-plays sc-text-secondary"}).findChildren()[1].get_text())
            else:
                d_data["num_streams"] = 0

            if track.find("span", {"class": "sc-truncate sc-tagContent"}):
                if transformer.fixstr(track.find("span", {"class": "sc-truncate sc-tagContent"}).get_text().lower())==data.find("h1", {"class": "tagsMain__title sc-py-1x sc-px-2x sc-mb-2x"}).get_text().split("#")[-1]:
                    d_data["main_tag"] = transformer.fixstr(track.find("span", {"class": "sc-truncate sc-tagContent"}).get_text())
                else:
                    d_data["main_tag"] = transformer.fixstr(track.find("span", {"class": "sc-truncate sc-tagContent"}).get_text())
                    d_data["taglist"] = data.find("h1", {"class": "tagsMain__title sc-py-1x sc-px-2x sc-mb-2x"}).get_text().split("#")[-1]
            else:
                d_data["main_tag"] = "Null"
                d_data["taglist"] = data.find("h1", {"class": "tagsMain__title sc-py-1x sc-px-2x sc-mb-2x"}).get_text().split("#")[-1]

            if track.find("a", {"class": "sc-ministats sc-ministats-small sc-link-secondary sc-text-h4 sc-ministats-followers "}):
                d_data["num_abonnes"] = transformer.fixinteger(track.find("a", {"class": "sc-ministats sc-ministats-small sc-link-secondary sc-text-h4 sc-ministats-followers "}).findChildren()[1].get_text())
            else:
                d_data["num_abonnes"] = 0

            l.info("Nouvelle ligne :")
            l.info(d_data)
            l.info("")

            datas.append(d_data)

        l.info("<<FIN EXTRACTION>>")

        return datas
    
    def transformJSONCollectionToRowData(data):
        
        @staticmethod
        def fixTaglist(str):
            if str:
                strlist = str.replace(r"\"", "").replace('"', '').replace(" ", ",").lower()
                return strlist
            else:
                return 'null'
        @staticmethod
        def fixint(value):
            return 0 if value is None else value
        
        n = 0
        datas=[]
        
        l.info("<<DEBUT TRANSFORMATION>>")
        for item in data:
            n = n + 1
            d_data = {
                "title": transformer.fixstr(item["title"]),
                "artist": transformer.fixstr(item["user"]["username"].lower()),
                "num_abonne": item["user"]["followers_count"],
                "date": transformer.fixdate(item["created_at"]),
                "num_likes": fixint(item["likes_count"]),
                "num_comments": fixint(item["comment_count"]),
                "num_streams": fixint(item["playback_count"]),
                "main_tag": transformer.fixstr(item["genre"]) if item["genre"] != "" else "null",
                "taglist" : fixTaglist(transformer.fixstr(item["tag_list"])) if item["tag_list"] != "" else "null"
            }
            l.info(f"Track : {n}\n {d_data}")
            
            datas.append(d_data)
        l.info(f"Nb de requête : {n}")
        l.info("")
        l.info("<<FIN TRANSFORMATION>>")
        l.info("")
        return datas