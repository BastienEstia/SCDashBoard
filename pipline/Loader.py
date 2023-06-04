import Connect as co
from psycopg2 import errors as e
import logging as l 

l.basicConfig(filename='pipline/logs/Loader.log', filemode='w', format='%(asctime)s %(message)s', encoding='UTF-8', level=l.INFO)

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

    def updateSet(cols, where, do = None):  
        # sourcery skip: instance-method-first-arg-name
        key_list = [k  for (k, val) in cols.items()]
        set_list = f"{key_list[0]} = {cols[key_list[0]]}"
        for i in range(1,len(key_list)):
            set_list = f"{set_list}, {key_list[i]} = {cols[key_list[i]]}"
        for i in range(1,len(key_list)-1):
            set_list2 = f"{set_list}, {key_list[i]} = {cols[key_list[i]]}"

        return (
            f"UPDATE SET {set_list} WHERE {where}"
            if do is None
            else f"UPDATE SET {set_list} WHERE {where} ON CONCLICT {do[key_list[-1]]} DO UPDATE SET {set_list2} WHERE {where}"
        )
    
    def load(data) -> None:  # sourcery skip: or-if-exp-identity, replace-interpolation-with-fstring, swap-if-expression
        l.info("<<DEBUT LOADING>>")
        l.info("")

        conn = co.connect.connection()
        l.info('Connexion à la base de données établie !')
        l.info("")

        cur = conn.cursor()

        #Insertion du tag "Null" pour éviter d'avoir des listes vide de tags
        sql_tags = (
                    "INSERT INTO public.tags(tag_name) VALUES ('null') ON CONFLICT DO NOTHING;"
                    )
        cur.execute(sql_tags)
        l.info("Requête de préparation pour le tag Null : %s" %(sql_tags))
        l.info("")

        # DEBUT DES REQUETES D'INSERTION --------------------------------------------------------------------------------------------------------
        l.info("DEBUT REQUÊTES INSERTION")
        l.info("")
        
        for i in range(len(data)):
            try:
    ############################################## Requête d'insertion table artiste ##############################################

                try:

                    sql = loader.insert(
                        "public.artists",
                        {
                            "artist_name": f"'{data[i]['artist']}'",
                            "num_sub": f"'{data[i]['num_abonne']}'"
                        }
                    )
                    cur.execute(sql)
                    l.info("Requête %d artiste : %s" %(i,sql))
                    l.info("")

                except UnicodeEncodeError as error:

                    l.error(f"Probleme enconding data dans la requête : {error.args[1]}")
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
                    l.error("Requête %d artiste avec null : %s" %(i,sql))
                    l.info("")

    ############################################## Requête d'insertion table tags ##############################################

                try:    
                    
                    sql = loader.insert(
                        "public.tags",
                        {
                            "tag_name": f"'{data[i]['main_tag'].lower()}'"
                        }
                    )
                    
                    cur.execute(sql)
                    l.info("Requête %d tag : %s" %(i,sql))
                    l.info("")

                except UnicodeEncodeError as error:

                    l.error(f"Probleme enconding data dans la requête : {error.args[1]}")
                    #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                    data[i]["main_tag"] = "null"  

                    sql = loader.insert(
                        "public.tags",
                        {
                            "tag_name": f"'{data[i]['main_tag'].lower()}'"
                        }
                    )
                    cur.execute(sql)
                    l.error("Requête %d tag avec Null : %s" %(i,sql))
                    l.info("")
                    
                for item in data[i]["taglist"].split(","):
                    
                    try:
                        sql = loader.insert(
                            "public.tags",
                            {
                                "tag_name":f"'{item}'"
                            }
                        )
                        l.info("Requête %d tag : %s" %(i,sql))
                        cur.execute(sql)
                        l.info("")
                    
                    except (UnicodeEncodeError) as error:
                        l.error(f"Probleme dans la requête :\n {error}")
                        #Si un problème d'encodage et raise alors la valeur qui pose probleme sera remplacé par Null

                        sql = loader.insert(
                            "public.tags",
                            {
                                "tag_name":"'null'"
                            }
                        )
                        l.error("Requête %d tag null : %s" %(i,sql))
                        cur.execute(sql)
                        l.info("")

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
                            })"""
                        },
                        {
                            "title" : loader.updateSet(
                            {
                                "num_likes": f"'{data[i]['num_likes']}'", 
                                "num_comments": f"'{data[i]['num_comments']}'",
                                "num_streams": f"'{data[i]['num_streams']}'"
                            },
                            f"tracks.title = '{data[i]['title']}'"
                            )
                        }
                    )
                    l.info("Requête %d track : %s" %(i,sql))
                    l.info("")
                    cur.execute(sql)

                except UnicodeEncodeError as error:

                    l.error(f"Probleme enconding data dans la requête : {error.args[1]}")
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
                    l.error("Requête %d track avec null : %s" %(i,sql))
                    l.info("")

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
                l.info("Requête %d tracks_artists : %s" %(i,sql_tracks_artists))
                cur.execute(sql_tracks_artists)
                l.info("")

    ############################################## Requête d'insertion table tracks_tags ##############################################

                for item in data[i]["taglist"].split(","):
                    
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
                                    f"tag_name = '{item}'"
                                )
                            })"""
                        }
                    )
                    l.info("Requête %d tracks_tags : %s" %(i,sql_tracks_tags))
                    l.info("")
                    cur.execute(sql_tracks_tags)

                conn.commit()
                l.info("Commit")           
                l.info("")
            except e.StringDataRightTruncation as error :
                l.warning(f'{error} | All requests for this tracks rollback')
                conn.rollback()
                continue
        
        l.info("Fin des requête d'insertion")
        l.info("")
        cur.close()
        l.info("Curseur fermé")
        conn.close()
        l.info("Connexion avec la base de données fermée")
        l.info("")
        l.info("<<FIN LOADING>>")
        
