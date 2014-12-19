import leadOverTimeLatest as lt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plotMaxLeadSmoothed(sport, step):
	data=lt.getData(sport)
	lead=lt.Lead(data,sport)
	scope=len(lead[0])
	m,t=lt.maxLeadTime(lead)
	df=pd.DataFrame(m,index=t)
	gr=df.groupby(df.index)
	avgm=gr.aggregate(np.mean)
	bins=np.arange(min(avgm.index),max(avgm.index)+1,step)
	groups=np.digitize(avgm.index.values.astype(int),bins)
	grouped=avgm.groupby(groups)
	groupAv=grouped.mean()
	groupAv.dropna()
	x=[bins[i-1] for i in groupAv.index]
	plt.scatter(x,groupAv)
	plt.xlim(xmin=0,xmax=scope)
	plt.ylim(ymin=0)
	plt.xlabel('Elapsed time, t')
	plt.ylabel('Maximum lead in a game')
	plt.show()
	