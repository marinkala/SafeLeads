import numpy as np
import sys


def getScope(sport):
	if sport=='NBA':
		scope=2880
		scores=91.99
	else:
		scope=3600
		if sport=='NHL':
			scores=3.81
		elif sport=='CFB':
			scores=8.28
		elif sport=='NFL':
			scores=7.34
	return scope, scores

#sport=sys.argv[1]
def Lead(sport):
	scope, scores=getScope(sport)
	games=scope*20
	bias=0.5

	#Generate scoring events and the scores associated with each event - which team score
	events=np.zeros(games*scope).reshape(games,scope)# the matrix that will store the events
	event_prob=scores/float(scope)
	rands=np.random.rand(games,scope) #random nums for all the seconds of all the games
	indices=np.transpose(np.flatnonzero(rands<event_prob)) #flat indices of where rands <event prob
	rands2=np.random.rand(len(indices)) #random nums for selecting who gets a point at each event
	points=-1+2*(rands2<bias)
	events.put(indices,points)

	#Translate the event data into the leads for each team
	lead=np.zeros(games*scope).reshape(games,scope) #matrix for storing the lead
	for i in xrange(games): #for each game
		lead[i]=np.cumsum(events[i])
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
			#switchInd=np.where((inLead[i]!=winner)&(inLead[i]!=0))[0]
			switchInd=np.where(inLead[i]!=winner)[0]
			if len(switchInd)==0:#no lead switch - the winning team scores at 0
				tr[i]=0
			else:
				lastInd=switchInd[-1]
				tr[i]=lastInd+1
				#this if-else is only needed if switchInd above has &(inLead[i]!=0)
				#if inLead[i,lastInd+1]==0:
				#	tr[i]=lastInd+2
				#else:
				#	tr[i]=lastInd+1 #last time winner team started to be in the lead
	rw=tr[tr>-1]
	rw=rw+1
	return rw
	#sr.tofile(sport+'RWlastLeadChange.txt',sep=',')