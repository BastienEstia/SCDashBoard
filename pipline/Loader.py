import Connect as co

# It takes a list of dictionaries and inserts the data into a PostgreSQL database

class loader:
    
    def insert(table, cols, do = None):
        # sourcery skip: instance-method-first-arg-name
        cols_key_list = [k  for (k, val) in cols.items()]
        if do : do_key_list = [k  for (k, val) in do.items()]

        attribs = cols_key_list[0]
        values = f"{cols[cols_key_list[0]]}"

        for i in range(1,len(cols_key_list)):
            
            attribs = f"{attribs},{cols_key_list[i]}"
            values = f"{values},{cols[cols_key_list[i]]}"

        do = f"ON CONFLICT ({do_key_list[0]}) DO {do[do_key_list[0]]}" if do else "ON CONFLICT DO NOTHING"

        return f"INSERT INTO {table}({attribs}) VALUES ({values}) {do};"
    
    def select(cols, table, where):
        # sourcery skip: instance-method-first-arg-name

        if cols == "*":
            if where:
                sql = f"SELECT * FROM {table} WHERE {where}"
            else:
                sql = f"SELECT * FROM {table}"
        else:
            attribs = cols[0]
            for i in range(1,len(cols)):
                attribs = f"{attribs}, {cols[i]}"
            if where:
                sql = f"SELECT {attribs} FROM {table} WHERE {where}"
            else:
                sql = f"SELECT {attribs} FROM {table}"
                
        return sql

    def updateSet(cols, where):  
        # sourcery skip: instance-method-first-arg-name
        key_list = [k  for (k, val) in cols.items()]
        set_list = f"{key_list[0]} = {cols[key_list[0]]}"
        for i in range(1,len(key_list)):
            set_list = f"{set_list}, {key_list[i]} = {cols[key_list[i]]}"
        
        return f"UPDATE SET {set_list} WHERE {where}"
    
    def load(data) -> None:  # sourcery skip: or-if-exp-identity, replace-interpolation-with-fstring, swap-if-expression
        print("")
        print("<<DEBUT LOADING>>")

        conn = co.connect.connection()
        print('Connexion à la base de données établie !')

        cur = conn.cursor()

        #Insertion du tag "Null" pour éviter d'avoir des listes vide de tags
        sql_tags = (
                    "INSERT INTO public.tags(tag_name) VALUES ('null') ON CONFLICT DO NOTHING;"
                    )
        cur.execute(sql_tags)
        print("Requête de préparation pour le tag Null : %s" %(sql_tags))

        # DEBUT DES REQUETES D'INSERTION --------------------------------------------------------------------------------------------------------
        print("DEBUT REQUÊTES INSERTION")
        for i in range(len(data)):

############################################## Requête d'insertion table artiste ##############################################

            try:

                sql = loader.insert(
                    "public.artists",
                    {
                        "artist_name": f"'{data[i]['artist']}'",
                        "num_sub": f"'{data[i]['num_abonnes']}'"
                    }
                )
                cur.execute(sql)
                print("")
                print("Requête %d artiste : %s" %(i,sql))

            except UnicodeEncodeError as error:

                print(f"Probleme enconding data dans la requête : {error.args[1]}")
                #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null
                data[i]["artist"] = "null"
                sql = loader.insert(
                    "public.artists",
                    {
                        "artist_name": f"'{data[i]['artist']}'",
                        "num_sub": f"'{data[i]['num_abonnes']}'"
                    }
                )
                cur.execute(sql)
                print("Requête %d artiste avec null : %s" %(i,sql))

############################################## Requête d'insertion table tags ##############################################

            for key in range(len(data[i])-7): # - les 7 tags précedents pour itérer seulement sur les tags
                try:    
                    
                    sql = loader.insert(
                        "public.tags",
                        {
                            "tag_name": f"'{data[i]['main_tag'].lower()}'"if key == 0 else f"'{data[i]['taglist'].lower()}'"
                        }
                    )
                    cur.execute(sql)
                    print("Requête %d tag : %s" %(i,sql))

                except UnicodeEncodeError as error:

                    print(f"Probleme enconding data dans la requête : {error.args[1]}")
                    #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                    if key == 0:
                        data[i]["main_tag"] = "null"  
                    else:
                        data[i]["taglist"] = "null"

                    sql = loader.insert(
                        "public.tags",
                        {
                            "tag_name": f"'{data[i]['main_tag'].lower()}'"if key == 0 else f"'{data[i]['taglist'].lower()}'"
                        }
                    )
                    cur.execute(sql)
                    print("Requête %d tag avec Null : %s" %(i,sql))

############################################## Requête d'insertion table tracks ##############################################

            try:

                sql = loader.insert(
                    "public.tracks", 
                    {
                        "title": f"'{data[i]['title']}'", 
                        "artists_id": f"""({loader.select(
                            ["artists_id"],
                            "public.artists",
                            f"artist_name = '{data[i]['artist']}'"
                        )
                        })""",
                        "datep": f"'{data[i]['date']}'",
                        "num_likes": f"'{data[i]['num_likes']}'",
                        "num_comments": f"'{data[i]['num_comments']}'",
                        "num_streams": f"'{data[i]['num_streams']}'",
                        "maintag": f"""({loader.select(
                                ["tags_id"],
                                "public.tags", 
                                f"tag_name = '{data[i]['main_tag'].lower()}'"
                            )
                        })""",
                        "taglist": f"""ARRAY({loader.select(
                                ["tags_id"],"public.tags", 
                                f"tag_name = '{data[i]['taglist'].lower()}'"
                            )
                        })""" if len(data[i]) != 8 else f"""ARRAY({loader.select(
                                ["tags_id"],
                                "public.tags", 
                                f"tag_name = 'null'"
                            )
                        })"""
                    },
                    {
                        "title" : loader.updateSet(
                        {
                            "num_likes": f"'{data[i]['num_likes']}'", 
                            "num_comments": f"'{data[i]['num_comments']}'",
                            "num_streams": f"'{data[i]['num_streams']}'", 
                            "taglist": f"""ARRAY({loader.select(
                                    ["taglist"], 
                                    "public.tracks", 
                                    f"title = '{data[i]['title'].lower()}'"
                                )
                            }) || ARRAY({loader.select(
                                    ["tags_id"],
                                    "public.tags",
                                    f"tag_name = '{data[i]['taglist'].lower() if len(data[i]) != 8 else 'null'}'"
                                )
                            })"""
                        },
                        f"tracks.title = '{data[i]['title']}'"
                        )
                    }
                )
                print("Requête %d track : %s" %(i,sql))
                cur.execute(sql)

            except UnicodeEncodeError as error:

                print(f"Probleme enconding data dans la requête : {error.args[1]}")
                #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null
                
                sql = loader.insert(
                    "public.tracks",
                    {
                        "title": 'Null',
                        "artists_id": f"""({loader.select(
                                ["artists_id"],
                                "public.artists",
                                f"artist_name = '{data[i]['artist']}'"
                            )
                    })""",
                    "datep": f"'{data[i]['date']}'",
                    "num_likes": f"'{data[i]['num_likes']}'",
                    "num_comments": f"'{data[i]['num_comments']}'",
                    "num_streams": f"'{data[i]['num_streams']}'",
                    "tags_id": f"""({loader.select(
                            ["tags_id"],
                            "public.tags",
                            f"tag_name = '{data[i]['main_tag'].lower()}'"
                        )
                    })"""
                })
                cur.execute(sql)
                print("Requête %d track avec null : %s" %(i,sql))

############################################## Requête d'insertion table tracks_artists ##############################################

            sql_tracks_artists = loader.insert(
                "public.tracks_artists", 
                {
                    "tracks_id": f"""({loader.select(
                            ["tracks_id"],
                            "tracks",
                            f"title = '{data[i]['title']}'"
                        )
                    })""",
                    "artists_id": f"""({loader.select(
                            ["artists_id"],
                            "artists",
                            f"artist_name = '{data[i]['artist']}'"
                        )
                    })"""
                }
            )
            cur.execute(sql_tracks_artists)
            print("Requête %d tracks_artists : %s" %(i,sql_tracks_artists))

############################################## Requête d'insertion table tracks_tags ##############################################

            for key in range(1,len(data[i])-7):
                
                sql_tracks_tags = loader.insert(
                    "public.tracks_tags", 
                    {
                        "tracks_id": f"""({loader.select(
                                ["tracks_id"],
                                "tracks",
                                f"title = '{data[i]['title']}'"
                            )
                        })""",
                        "tags_id": f"""({loader.select(
                                ["tags_id"],
                                "tags",
                                f"tag_name = '{data[i]['taglist']}'"
                            )
                        })"""
                    }
                )
                cur.execute(sql_tracks_tags)
                print("Requête %d tracks_tags : %s" %(i,sql_tracks_tags))

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