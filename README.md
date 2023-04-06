# SCDashBoard
GOAL : Create an ETL data pipline in python to store scraped data from SoundCloud.com into a PostgreSQL DataBase in order to feed a Metabase Dashboard of the tekno/rave scene of SoundCloud.

Technologies :

Scraping : Selenium/BeautifulSoup
ETL Pipline : Python class
Database : PostgreSQL relational
Dashboard : Metabase

Python ETL pipline class :

Extractor : Handle an extract() method that open a specific tag link from SC.com and scroll down on an infinite dynamic flux until a specific track creation date.
extract() return a beautifulsoup item that parse the the websource code after scrolling down. 

Transformer : Handle a transform() method that transform the web source code into a collection of python dictionaries with key/values of tracks.

Loader : Handle a loading() method that insert data from dictionary collection into postgreSQL DB by SQL insert request.

