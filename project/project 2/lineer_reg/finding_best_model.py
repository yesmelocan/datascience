import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error, r2_score
import warnings
# Veriyi yükleyin
data = pd.read_csv("scraped_data_orginal.csv")
data.rename(columns={"revunue": "revenue"}, inplace=True)

# Kullanıcının talimatlarına göre veri temizleme işlemleri
data = data.replace('--', 0)

# 'stock_name' sütununda NaN olan satırları kaldırın
data = data.dropna(subset=['stock_name'])
data = data.fillna(0)

# 'market cap' sütununu sayısal değere dönüştürme fonksiyonu
def convert_to_numeric(value):
    if pd.isna(value):
        return value
    value = str(value).strip()
    if value.endswith('%'):
        return float(value[:-1]) / 100
    if value.endswith('B'):
        return float(value[:-1]) * 1e9
    elif value.endswith('M'):
        return float(value[:-1]) * 1e6
    elif value.endswith('K') or value.endswith('k'):
        return float(value[:-1]) * 1e3
    elif value.endswith('T'):
        return float(value[:-1]) * 1e12
    else:
        return float(value)

data['market cap'] = data['market cap'].apply(convert_to_numeric)

# Özellikleri (X) ve hedef değişkeni (y) seçin
X = data[[ 'revenue', 'profit margin', 
          'Environmental Risk Score', ]]
y = data['market cap']
print(y.mean(),"market cap")
# Sayısal olmayan sütunları sayısal değere dönüştürün
X = X.applymap(convert_to_numeric)

# Tüm sütunların sayısal olduğundan ve sonsuz veya NaN değerlerin olmadığından emin olun
X = X.apply(pd.to_numeric, errors='coerce')
X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna()

# Hedef değişkenin de sayısal olduğundan emin olun
y = y.loc[X.index]


# Model fitting
linreg_model = LinearRegression()
linreg_model.fit(X, y)

# Print model intercept and coefficients
print("Intercept:", linreg_model.intercept_)
print("Coefficient:", linreg_model.coef_[0])    


model = sm.OLS(y,X)

results = model.fit()

print(results.summary())

pred = linreg_model.predict(X)

# RMSE Hesabı
print("RMSE:", np.sqrt(mean_squared_error(y, pred)))

# R2 Skor
print("R2 Score:", r2_score(y, pred))

