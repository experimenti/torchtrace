import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import utils
from sklearn.linear_model import LinearRegression


# =============================================================================
# load data
data = pd.read_csv('./results/s_trace.csv')  # edit path

total_inserted_bytes = data['size'].sum()

max_size_disk = data['size_on_disk'].max()
min_size_disk = data['size_on_disk'].min()
print("max {0}".format(max_size_disk))
print("min {0}".format(min_size_disk))

total_disk_consumed = max_size_disk - min_size_disk 
data['size_on_disk'].max() - data['size_on_disk'].min()
friendly_inserted_bytes = utils.bytes_2_human_readable(total_inserted_bytes)
print(friendly_inserted_bytes)

print("Total inserted serialized data: {0}".format(utils.bytes_2_human_readable(total_inserted_bytes)))
print("Total disk consumption: {0}".format(utils.bytes_2_human_readable(total_disk_consumed)))

data = data.sort_values(by=['time_stamp'])
data['total_serialized_bytes_inserted'] = data['size'].cumsum()

x = data['total_serialized_bytes_inserted']  # Memory usage
y = data['size_on_disk']  # Disk Consumed

# creat y_predict
model = LinearRegression(fit_intercept=True)

x = x[:, np.newaxis]
model.fit(x, y)

print('Disk Consumption Equation: = {} x Inserted Data (bytes) + {}'.format(model.coef_[0], model.intercept_))
size = float(input('enter size of Memory (MB) to predict Disk Consumption = '))
print('Disk Consumption Estimate = {} '.format(utils.bytes_2_human_readable(model.predict(size*1000000))))


