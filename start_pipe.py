from Pipline import Pipline
from datetime import datetime, timedelta

def main(args=None):
    pipe = Pipline(args, str(datetime.now()).split(".")[0], str( datetime.now() - timedelta(days=31)).split(".")[0])
    pipe.start()
    
if __name__ == "__main__":
    main()