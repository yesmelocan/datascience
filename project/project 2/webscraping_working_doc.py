
import pandas as pd
import re
import numpy as np
import time
import certifi
import urllib.request
import http.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
from bs4 import BeautifulSoup as bts


"""

def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent": "Chrome/125.0.6422.142"})
    soup = bts(result.text, "html.parser")
    return soup
"""
url = "https://finance.yahoo.com/quote/MSFT/"
driver = webdriver.Chrome()
driver.get(url)
html = bts(driver.page_source, "html.parser")
driver.quit()
 #html = getAndParseURL(html)

x = []

try:
    namecode = html.find('div',class_="left svelte-ezk9pj wrap")
    name = namecode.find("h1",class_="svelte-3a2v0c").text.split('(')[0]
    code = namecode.find("h1",class_="svelte-3a2v0c").text.split('(')[1]
except:
    name  = np.nan
    code = np.nan



try:
    price_span = html.find('div',class_="container svelte-aay0dk")
    price_span = price_span.find('fin-streamer', {'class': 'livePrice svelte-mgkamr'})
    price = price_span.get('data-value')
except:
    price = np.nan

x.append([name,code,price])






"""
target_div = html.find('div', class_='container svelte-mgkamr')
if target_div:
    price_span = target_div.find('fin-streamer', {'class': 'livePrice svelte-mgkamr'})
 
    if price_span:
        price = price_span.find(span)
        print(f"Extracted price: {price}")
    else:
        print("Price span element not found.")
else:
    print("Target div element not found.")
"""