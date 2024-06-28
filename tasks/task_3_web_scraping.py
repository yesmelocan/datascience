import requests
from bs4 import BeautifulSoup as bts
import pandas as pd
import re
import numpy as np
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import warnings
warnings.filterwarnings(action='ignore')
import os

def getAndParseURL(url):
    result = requests.get(url, headers={"User-Agent":"Chrome/125.0.6422.142 "}) # Safari/537.36. Chrome/103.0.0.0
    soup = bts(result.text, "html.parser")
    return soup
# URLs for today, tomorrow, and day 3 to day 7 forecasts
pages = [
    "https://www.accuweather.com/tr/us/lubbock/79401/weather-today/331131",
    "https://www.accuweather.com/tr/us/lubbock/79401/weather-tomorrow/331131"
]

for page in range(3, 8):
 
    pages.append("https://www.accuweather.com/tr/us/lubbock/79401/daily-weather-forecast/331131?day=" + str(page))

result = []

for url in pages:

    driver = webdriver.Chrome()
    driver.get(url)
    html = getAndParseURL(url)


    
    try:
        tarih = html.find("div",{"class":"subnav-pagination"}).div.text.split(",")[1].strip()
    except:
        tarih = np.nan
    
    try:
        gün = html.find("div",{"class":"subnav-pagination"}).div.text.split(",")[0].strip()
    except:
        gün = np.nan    
    
    try:
        gun_donemler = html.find_all("h2", {"class": "title"})
        gun_donem = gun_donemler[0].text.strip()
        gun_donem_night = gun_donemler[1].text.strip()
        
    except:
        gun_donem = np.nan
        gun_donem_night = np.nan
    
    try:
        temperature = html.find_all("div", {"class": "temperature"})
        temperature_day = temperature[0].text.strip().split("°")[0]+"°" 
        temperature_night = temperature[1].text.strip().split("°")[0]+"°" 
    except:
        temperature_day = np.nan
        temperature_night = np.nan
    
    try:
        wind = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Rüzgar" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    wind.append(value_span.text)
    except:
        wind = [np.nan]
    try:
        forecast = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Yağış Beklentisi" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    forecast.append(value_span.text)
    except:
        forecast = [np.nan]
    try:
        cot = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Gök Gürültülü Sağanak Yağış Olasılığı" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    cot.append(value_span.text)
    except:
        cot = [np.nan]
    
    try:
        precipitation = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Yağış" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    precipitation.append(value_span.text)
    except:
        cot = [np.nan]
    
    try:
        cloud = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Bulutlarla Kaplı" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    cloud.append(value_span.text)
    except:
        cloud = [np.nan]

    try:
        uv = []
        panel_items = html.find_all("p", {"class": "panel-item"})
        
        for item in panel_items:
            if "Maks UV İndeksi" in item.text:
                value_span = item.find("span", {"class": "value"})
                if value_span:
                    uv.append(value_span.text)
    except:
        uv = [np.nan]

    driver.quit()
    result.append([tarih,gün,gun_donem,temperature_day,wind[0],forecast[0],cot[0],precipitation[2],cloud[0],uv])
    result.append([tarih,gün,gun_donem_night,temperature_night,wind[2],forecast[1],cot[1],precipitation[5],cloud[1],np.nan])
    time.sleep(2)
df_columns = ["Tarih","Gün","Gün Dönemi","Sıcaklık","Rüzgar","Yağış Beklentisi","Gök Gürültülü Sağanak Yağış Olasılığı","Yağış","Bulutlarla Kaplı","Maks UV İndeksi"]

df = pd.DataFrame.from_records(result, columns=df_columns)


# Save the filtered data to a CSV file
df.to_csv('webscrapingodev.csv')

print(df)

    # Extract date information
"""
    date_div = html.find("div", {"class": "subnav-pagination"})
    if date_div:
        date_text = date_div.div.text.split(",")[1].strip()
        tarih.append(date_text)
    else:
        tarih.append(np.nan)
"""
