import numpy as np

def predict_dist(test):
	scope=2880
	edge=max(test[:,1])
	out=np.zeros(len(test))
	for i in xrange(len(test)):#for every test example
		dec_bound=0
		if test[i,1]==dec_bound:
			out[i]=0
		elif test[i,1]>dec_bound:
			out[i]=(test[i,1]-dec_bound)/(edge-dec_bound)
	return out