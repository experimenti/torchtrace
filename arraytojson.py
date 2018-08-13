import json
import numpy as np

def dynamicArrayBloat():

	iterations = 5 
	dict = {}
	attrib = 'attrib_'

	for k in range(0, iterations):

		D1, D2 = k + iterations, k + iterations	

		w1 = np.random.randn(D1, D2)

		for (x,y), value in np.ndenumerate(w1):
			print("x, y")
			print(x, y)

		#Dump data dict to jason
		j = json.dumps(w1.tolist()) 

		attrib = 'attrib_' + str(k) 
		dict[attrib]=w1.tolist()
		
		print(dict)

	return dict

result = dynamicArrayBloat()
print(result)


