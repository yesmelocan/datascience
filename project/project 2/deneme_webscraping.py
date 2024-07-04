
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
    price_span = html.find('div',class_="container svelte-aay0dk")
    price_span = price_span.find('fin-streamer', {'class': 'livePrice svelte-mgkamr'})
    price = price_span.get('data-value')
except:
    price = np.nan

x.append([price])
print(x)

"""

def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent": "Chrome/125.0.6422.142"})
    soup = bts(result.text, "html.parser")
    return soup
"""