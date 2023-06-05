import os
print(os.getcwd())

import pipline.Extractor as E
import pipline.Transformer as T
import pipline.Loader as L


class Pipline():
    
    def __init__(self, url, startd, stopd):
        self.url = url
        self.startd = startd
        self.stopd = stopd
        
    def start(self):
        
        extractor = E.extractor(self.url, None, self.startd, self.stopd)

        extracted_data = extractor.extractByAPI()

        transformed_data = T.transformer.transformJSONCollectionToRowData(extracted_data)

        L.loader.load(transformed_data)
