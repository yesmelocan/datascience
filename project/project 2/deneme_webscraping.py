
import numpy as np
import time
import urllib.request
import http.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup as bts



url = "https://finance.yahoo.com/quote/MSFT/sustainability/"
driver = webdriver.Chrome()
driver.get(url)
html = bts(driver.page_source, "html.parser")
driver.quit()
 #html = getAndParseURL(html)

x = []

valuation_p = html.find_all("div",{'class':"scoreRank svelte-y3c2sq"}) #.find_all("h4","border svelte-y3c2sq")

print(valuation_p)






try:
    valuation_p = html.find("div",{'class':"container svelte-1n4vnw8"}).find_all("h4","border svelte-y3c2sq")
    valuations = []
    for i in valuation_p:
        valuations.append(i.text)
        print(valuations)
except:
    print("lüzumu yok")
"""    
    esg_risk = valuations[0]
    enviromental_risk = valuations[6]
    social_risk = valuations[8]
    governance_risk =  
except:
    esg_risk = np.nan
    enviromental_risk = np.nan  
    social_risk = np.nan

x.append([esg_risk, enviromental_risk,social_risk])
print(x)
df = pd.DataFrame.from_records(result, columns=df_columns)
"""
"""

def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent": "Chrome/125.0.6422.142"})
    soup = bts(result.text, "html.parser")
    return soup
"""