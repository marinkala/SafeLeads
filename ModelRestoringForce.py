import numpy as np
import pandas
import sys

#sport=sys.argv[1]
def Lead(sport):
	folder='/Users/Ish/Documents/SafeLeads/Results/'
	path=folder+'/'+sport+'_res'

	ev_prob=pandas.Series.from_csv(path+'/'+sport+'_eventProb.csv',parse_dates=False)
	ev=np.array(ev_prob.tolist()) #np.array for event probabilities
	scope=len(ev_prob)
	score_dist=pandas.Series.from_csv(path+'/'+sport+'_scoreDist.csv',\
	parse_dates=False).values
	games=scope*50
	event_prob=np.tile(ev,(games,1)) #repeat ev_prob as row so can compare
	bias=0.5

	#Generate scoring events and the scores associated with each event - which team score
	events=np.zeros((games,scope))# the matrix that will store the events
	rands=np.random.rand(games,scope) #random nums for all the seconds of all the games
	indices=np.transpose(np.flatnonzero(rands<event_prob)) #flat indices of where rands <event prob
	#rands2=np.random.rand(len(indices)) #random nums for selecting who gets a point at each event
	#points=-1+2*(rands2<bias)
	events.put(indices,1)

	#Translate the event data into the leads for each team
	lead=np.zeros((games,scope)) #matrix for storing the lead
	for i in xrange(games): #for each game
		thisGameEvents=np.where(events[i]!=0)[0] #indices of events for this gamets
		scoredEvents=np.zeros(scope)
		for j in xrange(len(thisGameEvents)): #for each event in this game
			#uniformly at random pick a score from the score distribution
			r=np.random.rand()
			for l in xrange(len(score_dist)):
				if r<sum(score_dist[:l+1]):
					score=l+1
					break
			if thisGameEvents[j]!=0:#as long as the (first) event doesn't happen at time 0		
				bias=0.5-0.002*lead[i,thisGameEvents[j]-1] #based on lead just before this event
			points=-1+2*(np.random.rand()<bias) #which team gets the points
			if j<(len(thisGameEvents)-1): #not the time slice starting at last event
				fin=thisGameEvents[j+1]
			else: #time period starting at the last event
				fin=scope
			if thisGameEvents[j]!=0:#as long as (first) event doesn't happen at 0 - for indices
				lead[i,thisGameEvents[j]:fin]=lead[i,thisGameEvents[j]-1]+points*score
				#previous lead (a second ago)+current (directional) score
	return lead