import pandas
import matplotlib.pyplot as plt
import sys

dir=sys.argv[1]
folder='/Users/Ish/Documents/SafeLeads/Results/'
path=folder+dir+'_res'

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

data=pandas.DataFrame.from_csv(path+'/'+dir+'_all_clean.csv', \
	parse_dates=False)

def secs(tl):#to get seconds
	t=str(tl).split(':')
	sec=float(t[0])*60 +float(t[1])
	return sec

data['seconds']=data[time].apply(secs)
data['sec_term']=data[term]*term_len*60

if dir!='NHL':
	data['event_time']=data['sec_term']-data['seconds']
else:
	data['event_time']=data['sec_term']-term_len*60+data['seconds']
	
del data['seconds']
del data['sec_term']
data=data.sort(['SEASON','GAME_CODE','event_time']).reset_index(drop=True)

data.to_csv(path+'/'+dir+'_all_et.csv')

n=len(data.GAME_CODE.unique())#number of games
ev_prob=pandas.Series(data=0.0,index=xrange(1,scope+1))
for i in xrange(1,scope+1):
	ev_prob[i]=len(data[data.event_time==i])/float(n)
ev_prob.to_csv(path+'/'+dir+'_eventProb.csv')

#plt.plot(ev_prob)
#plt.ylim(ymin=0,ymax=max(ev_prob)+0.005)
#plt.xlim(xmin=0,xmax=scope+2)
#plt.xlabel('Elapsed time, t (seconds)')
#plt.ylabel('Pr(scoring event)')
#plt.title(dir)
#plt.show()