import pandas
import matplotlib.pyplot as plt
import sys

dir=sys.argv[1]
folder='/Users/Ish/Documents/SafeLeads/Results/'
path=folder+dir+'_res/'

data=pandas.DataFrame.from_csv(path+dir+'_all_clean.csv', \
	parse_dates=False)

scores=data.POINTS.unique()	
score_dist=pandas.Series(data=0.0, index=xrange(1,max(scores)+1))
for i in xrange(len(scores)):
    score_dist[scores[i]]=len(data[data.POINTS==scores[i]])/float(len(data))
#score_dist=score_dist[score_dist>0] #remove zero prob scores

score_dist.to_csv(path+dir+'_scoreDist.csv')