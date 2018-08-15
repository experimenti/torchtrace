import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import utils


# =============================================================================
# load data
data = pd.read_csv('./results/s_trace.csv')  # edit path


total_inserted_bytes = data['size'].sum()
total_disk_consumed = data['size_on_disk'].max() - data['size_on_disk'].min()
friendly_inserted_bytes = utils.bytes_2_human_readable(total_inserted_bytes)
print(friendly_inserted_bytes)

print("Total inserted serialized data: {0}".format(utils.bytes_2_human_readable(total_inserted_bytes)))
print("Total disk consumption: {0}".format(utils.bytes_2_human_readable(total_disk_consumed)))

data = data.sort_values(by=['time_stamp'])
data['total_write_events'] = data['size_on_disk'].cumsum()
data['total_serialized_bytes_inserted'] = data['size'].cumsum()

x = data['size']  # Memory usage
y = data['size_on_disk']  # Disk Consumed

# plot size on disk(output) VS commulative frequency of size(input)
plt.scatter(x, y)
plt.title('Real Data')
plt.xlabel('Size of Memory')
plt.ylabel('Disk Consumption')
plt.savefig("res")

# creat y_predict
from sklearn.linear_model import LinearRegression
model = LinearRegression(fit_intercept=True)

x = x[:, np.newaxis]
model.fit(x, y)

print(model.coef_)
print(model.intercept_)
print('Equation of linear:\t')
print(
    'Disk Consumption (byte) = {}Memory (byte) + {}'.format(model.coef_[0], model.intercept_))
print('the ratio of data = ')
size = int(input('enter size of Memory (bytes) to predict Disk Consumption = '))
print('DiskConsumption_pred = {} byte'.format(model.predict(size)[0]))


