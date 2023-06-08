import os
print(os.getcwd())

import pipline.Extractor as E
import pipline.Transformer as T
import pipline.Loader as L


class Pipline():
    
    def __init__(self, url, mode, startd, stopd):
        self.url = url
        self.mode = mode
        self.startd = startd
        self.stopd = stopd
        
        for file in os.listdir("/home/devadmin/Pythons_Scripts/MS_DB/SCDashBoard/tmp"):
            os.remove(f"/home/devadmin/Pythons_Scripts/MS_DB/SCDashBoard/tmp/{file}")
        
        
    def start(self):
        
        extractor = E.extractor(self.url, self.mode, None, self.startd, self.stopd)

        extracted_data = extractor.extractByAPI()
        
        transformer = T.transformer(self.mode)

        transformed_data = transformer.transformJSONCollectionToRowData(extracted_data)
        
        extracted_data = None

        L.loader.load(transformed_data)
