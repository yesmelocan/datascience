
import numpy as np
import time
import urllib.request
import http.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup as bts



url = "https://finance.yahoo.com/quote/MSFT/"
driver = webdriver.Chrome()
driver.get(url)
html = bts(driver.page_source, "html.parser")
driver.quit()
 #html = getAndParseURL(html)

x = []



try:
    valuation_p = html.find("div",{'class':"container svelte-1n4vnw8"}).find_all("p","value svelte-1n4vnw8")
    valuations = []
    for i in valuation_p:
        valuations.append(i.text)


    
    marketcap = valuations[0]
    price_book = valuations[6]
    ev_ebitda = valuations[8]
    
except:
    marketcap = np.nan
    price_book = np.nan  
    ev_ebitda = np.nan

x.append([marketcap, price_book,ev_ebitda])
print(x)

"""

def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent": "Chrome/125.0.6422.142"})
    soup = bts(result.text, "html.parser")
    return soup
"""