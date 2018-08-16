import json
import numpy as np

## build an array of D1, D2 dimensions
def jsonFromNumpyArray(ndarray):

	array_dict = {}

	iterations = ndarray.size
	print("Array Size {0}".format(iterations))

	array_dict = dict(np.ndenumerate(ndarray))
	#for k in range(1, iterations):


		# for (x,y), value in np.ndenumerate(ndarray):
		# 	x_attribute = 'x' + str(k) 
		# 	y_attribute = 'y' + str(k) 
		# 	element = x_attribute + '_' + y_attribute

		# 	dict[element]=ndarray[x, y]
		
	return array_dict



