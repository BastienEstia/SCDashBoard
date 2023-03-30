import os
print(os.getcwd())

import pipline.Extractor as E
import pipline.Transformer as T
import pipline.Loader as L

URL="https://soundcloud.com/tags/hardtek"
ITEM_NB = 9

extractor = E.extractor(URL, None, "2023-03-24 00:00:00")

extracted_data = extractor.extract()

transformed_data = T.transformer.transform(extracted_data)

L.loader.load(transformed_data)
