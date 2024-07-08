

import pandas as pd 

train = pd.read_csv("scraped_data_orginal.csv")

print(train[train["stock_code"]== "AMZN"]["price/book"])