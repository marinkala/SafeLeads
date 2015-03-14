import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def ScoringRate(sport):
	if sport=='NBA':
		scope=2880
		seasons='2002-2010'
	else:
		scope=3600
		seasons='2000-2009'

	ev_prob=pd.DataFrame.from_csv('/Users/Ish/Documents/SafeLeads/Results/'+sport+'_res/'+sport+'_eventProb.csv',\
header=None)

	fontSize=18
	window=10
	smoothEvProb=movingaverage(ev_prob[1],window)
	avg=np.mean(smoothEvProb)
	#y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=-100)
	#ax1.yaxis.set_major_formatter(y_formatter)
	plt.plot(smoothEvProb, linewidth=1.3)
	plt.hlines(avg, 0,scope, colors='red', linewidth=2)
	plt.xlim(xmin=0, xmax=scope)
	plt.ylim(ymin=0,ymax=0.006)
	plt.ylabel('Pr(scoring event)',fontsize=fontSize)#25 for NBA
	plt.tick_params(labelsize=fontSize)

	#f.subplots_adjust(left=0.16, right=0.95, top=0.95, bottom=0.11, hspace=0.00001) #16,13
	plt.show()