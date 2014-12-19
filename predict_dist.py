import numpy as np

def predict_dist(test):
	scope=2880
	edge=max(test[:,1])
	out=np.zeros(len(test))
	for i in xrange(len(test)):#for every test example
		dec_bound=(scope-test[i,0])**0.5+3
		if test[i,1]==dec_bound:
			out[i]=0.5
		elif test[i,1]>dec_bound:
			out[i]=0.5+(test[i,1]-dec_bound)/(2*(edge-dec_bound))
		elif test[i,1]<dec_bound:
			out[i]=0.5-(dec_bound-test[i,1])/(2*dec_bound)
	return out