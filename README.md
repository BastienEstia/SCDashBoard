# SCDashBoard
GOAL : Create an ETL data pipline in python to store scraped data from SoundCloud.com into a PostgreSQL DataBase in order to feed a Metabase Dashboard of the tekno/rave scene of SoundCloud.

Technologies :

Scraping : Selenium/BeautifulSoup
ETL Pipline : Python class
Database : PostgreSQL relational
Dashboard : Metabase

Python ETL pipline class :

Extractor : Handle an extractByWebPageSourceCode() method that open a specific tag link from SC.com and scroll down on an infinite dynamic flux until a specific track creation date and return a beautifulsoup item that parse the the websource code after scrolling down : but this is very slow and do not work when a large amount of track are created (i.e tag techo on SC)
New Extractor method named extractByAPI() not using SC API because it's closed but using API requests from AJAX update flows. It return a collection of JSON object

Transformer : Handle a transformPageSourceToRowData() method that transform the web source code into a collection of python dictionaries with key/values of tracks.
New Transformer method named transformJSONCollectionToRowData() that transform JSON tracks into row data with some rectification around data structure.

Loader : Handle a loading() method that insert data from dictionary collection into postgreSQL DB by SQL insert requests.

