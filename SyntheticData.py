import pandas
import random
import matplotlib.pyplot as plt
import sys
import numpy as np

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_res'

ev_prob=pandas.Series.from_csv(path+'/'+dir+'_eventProb.csv',\
	parse_dates=False)
scope=len(ev_prob)
#lead_prob=pandas.Series.from_csv(path+'/'+dir+'_probScoreGivenLead.csv',\
	#parse_dates=False)
#lead_prob=pandas.Series(data=0.5*np.ones(len(l)),index=l.index)
score_dist=pandas.Series.from_csv(path+'/'+dir+'_scoreDist.csv',\
	parse_dates=False)

iterations=10000 #number of simulated games
data=pandas.DataFrame()
for k in xrange(iterations):
	rands=[random.random() for r in xrange(scope)]
	event=rands<ev_prob
	n=sum(event)#number of events occuring in this game
	event_list=event[event==True]

	game=pandas.DataFrame(columns=['GAME_CODE','event_time','lead_before','TEAM_ID','POINTS','lead'],\
		index=xrange(n))
	for i in xrange(n):#for every event in this game
		game.GAME_CODE[i]=k
		game.event_time[i]=event_list.index[i]
		if i==0:#first event
			game.lead_before[i]=0 #set incoming lead for the first event to 0
			if random.random()<0.5:
				game.TEAM_ID[i]=1 #team 1 scores first event
			else:
				game.TEAM_ID[i]=-1
			leader=game.TEAM_ID[i] #team that scores first - starter
		else:
			game.lead_before[i]=game.lead[i-1]
			if random.random()<0.5:#lead_prob[game.lead_before[i]]:
				game.TEAM_ID[i]=game.TEAM_ID[i-1] #keep the same team scoring
			else:
				game.TEAM_ID[i]=-game.TEAM_ID[i-1] #switch the scoring team
		low=0
		high=0
		r=random.random()
		for j in xrange(len(score_dist)):
			high=low+score_dist.iloc[j]
			if (r>=low) & (r<high):
				game.POINTS[i]=score_dist.index[j]
			low+=score_dist.iloc[j]
		if i==0:
			game.lead[i]=game.POINTS[i]
		else:
			if game.TEAM_ID[i]==leader:
				game.lead[i]=game.lead[i-1]+game.POINTS[i]
			else:
				game.lead[i]=game.lead[i-1]-game.POINTS[i]
				#if (game.lead[i])<0:
				#	leader=-leader
	data=data.append(game).reset_index(drop=True)

#data.to_csv(path+'/Synth/'+dir+'_synthData0.7.csv')