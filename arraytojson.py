import json
import numpy as np

## build an array of D1, D2 dimensions
def numpyArrayToJson(iterations=5):

	dict = {}

	for k in range(1, iterations):

		D1, D2 = k + iterations, k + iterations	

		w1 = np.random.randn(D1, D2)

		for (x,y), value in np.ndenumerate(w1):
			x_attribute = 'x' + str(k) 
			y_attribute = 'y' + str(k) 
			element = x_attribute + '_' + y_attribute

			dict[element]=w1[x, y]
		
	return dict



