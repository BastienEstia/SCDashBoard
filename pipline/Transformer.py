# It's a class that transforms data

class transformer:
    
    def __init__(self):
        pass
            
    def fixstr(self):
        return self.replace("'", "''")

    def fixdate(self):
        jour = self.split("T")[0]
        heure = self.split("T")[1].split(".")[0]
        return f'{jour} {heure}'

    def fixinteger(self):
        try:
            strlist = self.split(".")
            if self.find("K") != -1:
                new_int = int(strlist[0])*1000 + int(strlist[1].split("K")[0])*100
            elif self.find("M") != -1:
                new_int = int(strlist[0])*1000000 + int(strlist[1].split("M")[0])*100000
            else:
                new_int = int(''.join(strlist))
        except ValueError:
            strlist = self.split(",")
            if self.find("K") != -1:
                new_int = int(strlist[0])*1000 + int(strlist[1].split("K")[0])*100
            elif self.find("M") != -1:
                new_int = int(strlist[0])*1000000 + int(strlist[1].split("M")[0])*100000
            else:
                new_int = int(''.join(strlist))
        return new_int

    def transform(data):
        # sourcery skip: extract-duplicate-method, instance-method-first-arg-name
        print("")
        print("<<DEBUT TRANSFORMATION>>")

        print("Récupération des items contnenant les données...")
        tracks = data.find_all("li", {"class": "soundList__item"})

        print("Transformation des données... ")
        print("")
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