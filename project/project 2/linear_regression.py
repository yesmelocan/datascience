import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


train = pd.read_csv("scraped_data_orginal.csv")

def convert_to_float(x):
    if 'T' in x:
        return float(x.replace('T', '')) * 1e12
    elif 'B' in x:
        return float(x.replace('B', '')) * 1e9
    elif 'M' in x:
        return float(x.replace('M', '')) * 1e6
    return float(x)




"""
print(train.head())
print(train.info())
"""

train.rename(columns = {"revunue" : "revenue"},inplace=True)
train = train.dropna(subset = ["stock_name"])

#print(train[train["revenue"] == "--"])

train['revenue'] = train['revenue'].apply(convert_to_float)
train['market cap'] = train['market cap'].apply(convert_to_float)

train = train.dropna(subset=["market cap",'price','revenue', 'Environmental Risk Score'])



# X ve Y değişkenlerimizi oluşturma
X = train.loc[:,['price','revenue', 'Environmental Risk Score']]
y = train["market cap"]

# Train/Test Ayrımı
X_train, x_test, Y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train/Validation Ayrımı
x_train, x_cv, y_train, y_cv = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
"""
print('X Train:', x_train.shape)
print('X Validation:', x_cv.shape)
print('X test:', x_test.shape)
"""

# Modeli Oluşturma
lreg = LinearRegression()

lreg.fit(x_train, y_train)

pred = lreg.predict(x_cv)

# RMSE Hesabı
print("RMSE:", np.sqrt(mean_squared_error(y_cv, pred)))

# R2 Skor
print("R2 Score:", r2_score(y_cv, pred))


"""
print(lreg.coef_,"coef")
sns.histplot(y_train)
plt.show()
"""
plt.figure(figsize=[18,5])

plt.suptitle('Revenue Distribution', fontsize = 16)

plt.subplot(1,2,1)
sns.histplot(data = train['revenue'], kde=True)
plt.title('Train')
plt.show()

plt.figure(figsize=[18,5])
sns.boxplot(x=train['Environmental Risk Score'])
plt.show()