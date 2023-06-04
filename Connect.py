import psycopg2 as ps
from configparser import ConfigParser

def config(filename="./database.ini", section="postgresql"):
    # sourcery skip: raise-specific-error
    """
    It reads a configuration file and returns a dictionary of the parameters in the specified section
    
    :param filename: The name of the file that contains the configuration, defaults to Python_Projects\SCDashBoard\database.ini (optional)
    :param section: The name of the section in the configuration file, defaults to postgresql (optional)
    :return: A dictionary of the parameters in the section of the ini file.
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    try:
        if not parser.has_section(section):
            raise Exception(f'Section {section} not found in the {filename} file')
        params = parser.items(section)
        return {param[0]: param[1] for param in params}
    except Exception as error:
        print(error)
        return -1
class connect(ps._psycopg.connection):
    
    def __init__(self):
        pass
    
    def connection():
        """
        It connects to the database, creates a cursor, prints the database version, and then closes the
        cursor
        :return: The connection object.
        """
        """ Connect to the PostgreSQL database server"""
        conn = None
        try:

            # read connection parameters
            params = config()

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            conn = ps.connect(**params)

            # create a cursor
            cur = conn.cursor()

            print('PostgreSQL database version : ')
            cur.execute('SELECT version()')

            db_version = cur.fetchone()
            print(db_version)

            cur.close()
        except (Exception, ps.DatabaseError) as error:
            print(f"erreur : {error}")
            return -1
        return conn
        