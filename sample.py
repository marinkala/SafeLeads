import random
import pandas
import numpy as np
#bias=0.01 for 4th quarter
#bias=0.005 for 2nd half
#bias=0.003 for all game

data=pandas.DataFrame(X,index=None,columns=None)
n=len(data)
bias=0.003*np.ones(n)
rands=[random.random() for r in xrange(n)]
data['sample']=rands<bias
sample=data[data.sample==True]
del sample['sample']
sample.to_csv('timeLeadSafeAll_sample.csv',index=False, header=False)
