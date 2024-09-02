import requests
from bs4 import BeautifulSoup as bts
import pandas as pd
import re
import numpy as np
import time
import certifi

#print(certifi.where())


def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent":"Chrome/125.0.6422.142"})
    soup = bts(result.text, "html.parser")
    return soup

html = getAndParseURL("https://yokatlas.yok.gov.tr/lisans-anasayfa.php")
