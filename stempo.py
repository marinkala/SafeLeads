import pandas
import matplotlib.pyplot as plt
import sys

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_res/Synth'

if (dir=='NBA') | (dir=='NHL'):
	term='PERIOD'
	if (dir=='NBA'):
		term_len=12
		scope=2880
	else: #NHL
		term_len=20
		scope=3600
else: #football
	term='QUARTER'
	term_len=15
	scope=3600
	
if (dir=='NHL'):
	time='TIME_IN'
else:
	time='TIME_LEFT'

data=pandas.DataFrame.from_csv(path+'/'+dir+'_synthData.csv', \
	parse_dates=False)

n=len(data.GAME_CODE.unique())#number of games
ev_prob=pandas.Series(data=0.0,index=xrange(1,scope+1))
for i in xrange(1,scope+1):
	ev_prob[i]=len(data[data.event_time==i])/float(n)

plt.plot(ev_prob)
plt.ylim(ymin=0,ymax=max(ev_prob)+0.005)
plt.xlim(xmin=0,xmax=scope+2)
plt.xlabel('Elapsed time, t (seconds)')
plt.ylabel('Pr(scoring event)')
plt.title('Synthetic '+dir)
plt.show()