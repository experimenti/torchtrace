import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


matplotlib.use('agg')

# =============================================================================
#load data
data = pd.read_csv('./results/s_trace.csv') #edit path
data = data.sort_values(by=['time_stamp'])
data['cummulative_frequency'] = data['size'].cumsum()
print(data.describe())
print(data.head)

#correlation data
corr_data = data.corr()
print(corr_data['cummulative_frequency'].sort_values(ascending=False)) 
print(corr_data['size_on_disk'].sort_values(ascending=False)) 
# from data correlation result can summarize that the data is high bias
# =============================================================================

x = data['cummulative_frequency'] #Memory usage
y = data['size_on_disk'] #Disk Consumed

#plot size on disk(output) VS commulative frequency of size(input)
plt.scatter(x, y)
plt.title('Real Data')
plt.xlabel('Size of Memory')
plt.ylabel('Disk Consumption')
plt.savefig("res")

#creat y_predict
from sklearn.linear_model import LinearRegression
model = LinearRegression(fit_intercept=True)

x = x[:, np.newaxis]
model.fit(x, y)

print(model.coef_)
print(model.intercept_)
print('Equation of linear:\t')
print('Disk Consumption (byte) = {}Memory (byte) + {}'.format(model.coef_[0], model.intercept_))
print('the ratio of data = ')
size = int(input('enter size of Memory (bytes) to predict Disk Consumption = '))
print('DiskConsumption_pred = {} byte'.format(model.predict(size)[0]))