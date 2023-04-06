import os
print(os.getcwd())

import pipline.Extractor as E
import pipline.Transformer as T
import pipline.Loader as L
import time

URL="https://soundcloud.com/tags/acidcore"
ITEM_NB = 9

extractor = E.extractor(URL, None, "2023-04-05 13:00:00", "2023-04-04 13:00:00")

extracted_data = extractor.extractByAPI()

transformed_data = T.transformer.transformJSONCollectionToRowData(extracted_data)

L.loader.load(transformed_data)
