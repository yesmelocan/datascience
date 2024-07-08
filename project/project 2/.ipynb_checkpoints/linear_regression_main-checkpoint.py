import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi yükleyin
data = pd.read_csv("/mnt/data/scraped_data_orginal.csv")
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

# Korelasyon matrisini hesaplayın
corr_matrix = X.corr()

# Korelasyon matrisini çizdirin
plt.figure(figsize=(14, 10))
sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=0.5, annot_kws={"size": 12, "color": "black"})
plt.title('Feature Correlation Matrix')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()  # Layout'u sıkılaştır
plt.show()



# Plotting the correlation matrix
plt.figure(figsize=(10, 8))
corr_matrix = data.corr()
sns.heatmap(corr_matrix, annot=True, cmap='seismic',  vmin=-1, vmax=1,fmt=".1f", annot_kws={"size": 12})
plt.title("Correlation Matrix")
plt.show()
print(corr_matrix)
print("Verilerdeki eksik veya hatalı değerler:")
print(data.isnull().sum())
print("\nVerilerin genel durumu:")
print(data.describe())
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
