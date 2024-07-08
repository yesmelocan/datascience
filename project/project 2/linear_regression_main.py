import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import statsmodels.api as sm

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

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and fit the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)
# Predict and evaluate the model
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"Initial R-squared value: {r2}")

coefficients = model.coef_
intercept = model.intercept_

print(coefficients, intercept)

# Korelasyon matrisini hesaplayın
corr_matrix = X.corr()
print("coefficients:",corr_matrix)
# Korelasyon matrisini çizdirin
plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5, annot_kws={"size": 12, "color": "black"})
plt.title('Feature Correlation Matrix')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()  # Layout'u sıkılaştır
plt.show()


ols = sm.OLS(y_train, X_train)
ols_model = ols.fit()
#print(ols_model.summary())
"""
lreg = LinearRegression()

lreg.fit(X_train, y_train)

pred = lreg.predict(X_train)
"""
from sklearn.linear_model import Ridge

from sklearn.preprocessing import MinMaxScaler

lreg2 = LinearRegression()

minmax_scale = MinMaxScaler()
x_train_ss = minmax_scale.fit_transform(X_train)
x_cv_ss = minmax_scale.transform(x_cv)

lreg2.fit(x_train_ss, y_train)

pred = lreg2.predict(x_cv_ss)

# R2 Skor
print("R2 Score:", r2_score(y_cv, pred))
print("Validation Score:", r2_score(y_cv, pred))
# R2 Skor
#print("R2 Score:", r2_score(y_train, pred))

"""
# Plotting the correlation matrix
plt.figure(figsize=(10, 8))
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='seismic',  vmin=-1, vmax=1,fmt=".1f", annot_kws={"size": 12})
plt.title("Correlation Matrix")
plt.show()
"""

#scatter plot
"""

sns.pairplot(data)
plt.show()
"""
"""
# Create scatter plots for each feature against the market cap
fig, axs = plt.subplots(4, 2, figsize=(15, 20))
axs = axs.flatten()




for i, col in enumerate(X.columns):
    axs[i].scatter(X[col], y, alpha=0.5)
    axs[i].set_title(f'{col} vs Market Cap')
    axs[i].set_xlabel(col)
    axs[i].set_ylabel('Market Cap')

plt.tight_layout()
plt.show()
"""