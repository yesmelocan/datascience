import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.metrics import mean_squared_error, r2_score
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
X = data[['price', 'revenue', 'profit margin', 'price/book', 'Enterprise Value/EBITDA', 
          'Environmental Risk Score', 'Social Risk Score', 'Governance Risk Score']]
y = data['market cap']

# Sayısal olmayan sütunları sayısal değere dönüştürün
X = X.applymap(convert_to_numeric)

# Tüm sütunların sayısal olduğundan ve sonsuz veya NaN değerlerin olmadığından emin olun
X = X.apply(pd.to_numeric, errors='coerce')
X = X.replace([np.inf, -np.inf], np.nan)
X = X.dropna()

# Hedef değişkenin de sayısal olduğundan emin olun
y = y.loc[X.index]



model = LinearRegression()

# Perform Sequential Feature Selection
sfs = SequentialFeatureSelector(model, n_features_to_select='auto', direction='forward')
sfs.fit(X, y)

# Get the selected features
selected_features = X.columns[sfs.get_support()]
print(selected_features)
# Train the model with selected features
X_selected = X[selected_features]
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Calculate performance metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(selected_features, mse, r2)