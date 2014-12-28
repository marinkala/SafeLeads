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
	games=scope*10
	event_prob=np.tile(ev,(games,1)) #repeat ev_prob as row so can compare
	bias=0.5

	#Generate scoring events and the scores associated with each event - which team score
	events=np.zeros(games*scope).reshape(games,scope)# the matrix that will store the events
	rands=np.random.rand(games,scope) #random nums for all the seconds of all the games
	indices=np.transpose(np.flatnonzero(rands<event_prob)) #flat indices of where rands <event prob
	rands2=np.random.rand(len(indices)) #random nums for selecting who gets a point at each event
	points=-1+2*(rands2<bias)
	events.put(indices,points)

	#Translate the event data into the leads for each team
	lead=np.zeros(games*scope).reshape(games,scope) #matrix for storing the lead
	for i in xrange(games): #for each game
		thisGameEvents=np.where(events[i]!=0)[0] #indices of events for this game
		scoredEvents=np.zeros(scope)
		for j in xrange(len(thisGameEvents)): #for each event in this game
			#uniformly at random pick a score from the score distribution
			r=np.random.rand()
			for l in xrange(len(score_dist)):
				if r<sum(score_dist[:l+1]):
					score=l+1
					break
			if j<(len(thisGameEvents)-1): #not the time slice starting at last event
				inEvTime=events[i][thisGameEvents[j]:thisGameEvents[j+1]]#till next event
				scoredEvents[thisGameEvents[j]:thisGameEvents[j+1]]=inEvTime*score
			else: #time period starting at the last event
				inEvTime=events[i][thisGameEvents[j]:] #till the end
				scoredEvents[thisGameEvents[j]:]=inEvTime*score
		lead[i]=np.cumsum(scoredEvents)
	return lead
	
def inLead(lead):
	games=len(lead)
	scope=len(lead[0])

	#Which team is in the lead at any given time
	inLead=np.zeros(games*scope).reshape(games,scope) 
	inLead[lead>0]=1 #team who scored first is in the lead
	inLead[lead<0]=-1
	return inLead
	
def lastChange(inLead):
	games=len(inLead)
	tr=-1*np.ones(games) #array for safe lead times - 1 for ties
	for i in xrange(games): #for each game
		winner=inLead[i,-1] #the last element of inLead shows who's the winner
		if winner!=0: #not a tie
			switchInd=np.where(inLead[i]!=winner)[0]
			if len(switchInd)==0:#no lead switch - the winning team scores at 0
				tr[i]=0
			else:
				lastInd=switchInd[-1]
				tr[i]=lastInd+1
	sr=tr[tr>-1]
	sr=sr+1
	return sr