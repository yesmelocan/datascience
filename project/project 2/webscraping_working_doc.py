
import pandas as pd
import re
import numpy as np
import time
import certifi
import urllib.request
import http.client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup as bts
from bs4.element import Tag
import random

excel = pd.read_excel("sp500.xlsx",sheet_name ="Sayfa1")

def get_html_soup(url):
    driver = webdriver.Chrome()
    driver.get(url)
    soup = bts(driver.page_source, "html.parser")
    driver.quit()
    return soup


#url = "https://finance.yahoo.com/quote/MSFT/"
#url_risk = "https://finance.yahoo.com/quote/MSFT/sustainability/"
#links = ["https://finance.yahoo.com/quote/MSFT/","https://finance.yahoo.com/quote/AAPL/"]

links = []
for symbol in excel["Symbol"]:
    links.append("https://finance.yahoo.com/quote/" +symbol + "/")


x = [] 
for url in links:
    html = get_html_soup(url)
    html_risk = get_html_soup(url + "sustainability/")
    

   



    

    try:
        namecode = html.find('div',class_="left svelte-ezk9pj wrap")
        name = namecode.find("h1",class_="svelte-3a2v0c").text.split('(')[0].strip()
        code = namecode.find("h1",class_="svelte-3a2v0c").text.split('(')[1].split(')')[0].strip()
    except:
        name  = np.nan
        code = np.nan


    try:
        price_span = html.find('div',class_="container svelte-aay0dk")
        price_span = price_span.find('fin-streamer', {'class': 'livePrice svelte-mgkamr'})
        price = price_span.get('data-value')
    except:
        price = np.nan

    try:
        price_span = html.find('div',class_="highlights svelte-lc8fp0").find_all('p', {'class': 'value svelte-lc8fp0'})
        revenues = []
        margin = [] 
        for i in price_span:       
            revenues.append(i.text)
        revenue = revenues[3]
        margin =  revenues[0]  #profit margin
    except:
        revenue = np.nan    
        margin = np.nan

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

    try:
        valuation_p = html_risk.find_all("div", {'class': "scoreRank svelte-y3c2sq"})
        values = []
        for val in valuation_p:
            h4_tag = val.find("h4")
            if h4_tag and isinstance(h4_tag, Tag):
                values.append(h4_tag.text.strip())
        environment_score = values[1]
        social_score = values[2]
        governance_score = values[3]
    except:
        environment_score = np.nan
        social_score = np.nan
        governance_score = np.nan


    df_columns = ["stock_name","stock_code","price","revunue","profit margin","market cap","price/book","Enterprise Value/EBITDA"
    ,"Environmental Risk Score","Social Risk Score","Governance Risk Score"]
    x.append([name,code,price,revenue,margin,marketcap,price_book,ev_ebitda,environment_score,social_score,governance_score])


    df = pd.DataFrame.from_records(x, columns=df_columns)

    time.sleep(random.uniform(5,15))

df.to_csv("scraped_data.csv", index=False)

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