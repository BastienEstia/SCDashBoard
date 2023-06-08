from Pipline import Pipline
from datetime import datetime, timedelta
import sys

def main(argv):
    
    URL = "https://soundcloud.com/tags/acidcore"
    if len(argv)==2:
        pipe = Pipline(argv[1], "wmf",str(datetime.now()).split(".")[0], str(datetime.now() - timedelta(days=31)).split(".")[0])
    else:
        pipe = Pipline(URL, "wmf",str(datetime.now()).split(".")[0], str(datetime.now() - timedelta(days=15)).split(".")[0])
    pipe.start()
    
if __name__ == "__main__":
    main(sys.argv)