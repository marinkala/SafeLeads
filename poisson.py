import pandas
import math
from matplotlib import pyplot as plt
import sys

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_res'

data=pandas.DataFrame.from_csv(path+'/'+dir+'_all_lead.csv', \
	parse_dates=False)
	
if dir=='NBA':
	duration=2880
	start=40
else:
	duration=3600
	start=0
	
grouped=data.groupby(['SEASON','GAME_CODE'])
num_events=[]
for name, group in grouped:
	num_events.append(len(group))
	
events_df=pandas.DataFrame(num_events,columns=['num_events'])
ev_grouped=events_df.groupby('num_events')
ev=[]
freq=[]
n=len(events_df)

for name, group in ev_grouped:
    ev.append(name)
    freq.append(len(group)/float(n))

lambdT=events_df.mean().values[0]
lambd=lambdT/duration

p=[]
for k in xrange(max(num_events)):
    p.append(math.exp(-lambdT)*(lambdT**k)/math.factorial(k))

plt.scatter(ev,freq)
plt.plot(xrange(max(num_events)),p,'--r')
plt.ylim(ymin=0)
plt.xlim(xmin=start)
plt.xlabel('Total scoring events, e')
plt.ylabel('Pr(E=e)')
plt.title(dir)
plt.show()