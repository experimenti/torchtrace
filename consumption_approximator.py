import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd


# =============================================================================
#load data
data = pd.read_csv('./results/s_trace.csv') #edit path


total_inserted_bytes = data['size'].sum()
print("Total inserted serialized data (bytes): {0}".format(total_inserted_bytes))

data = data.sort_values(by=['time_stamp'])
data['total_write_events'] = data['size_on_disk'].cumsum()
data['total_serialized_bytes_inserted'] = data['size'].cumsum() 

print('Total serialized data insert size: {0} '.format(str(data['total_serialized_bytes_inserted'])))
print('Total disk write events: {0} '.format(str(data['total_write_events'])))

# print(type(data))

# print(data.describe())
# print(data.head)

# print('Cummulative Sum: {0} '.format(data['cummulative_sum'])

# correlation data

#corr_data = data.corr()

# print(corr_data['cummulative_frequency'].sort_values(ascending=False)) 
# print(corr_data['size_on_disk'].sort_values(ascending=False)) 

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
