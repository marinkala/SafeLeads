import numpy as np

scope=2880
games=scope*5
score_dist=[0.090889895, 0.745225242935816, 0.163039353008472, \
0.000823665502613431,0.0000209329354255347, 9.10127627197161E-07]
bias=0.5

#Generate scoring events and the scores associated with each event - which team score
events=np.zeros(games*scope).reshape(games,scope)# the matrix that will store the events
event_prob=91.99/float(scope)
rands=np.random.rand(games,scope) #random nums for all the seconds of all the games
indices=np.transpose(np.flatnonzero(rands<event_prob)) #flat indices of where rands <event prob
events.put(indices,1) #put 1 where there is an event

#Translate the event data into the leads for each team
#Get the safe lead time for each game
lead=np.zeros(games*scope).reshape(games,scope) #matrix for storing the lead
#from the perspective of team A!!!!!!
t=np.zeros(games) #array for safe lead times
for i in xrange(games): #for each game
	inds=np.nonzero(events[i])[0] #indices of the events for this particular game
	for j in xrange(len(inds)): #for each event in that game
		if lead[i,inds[j]-1]!=0: #if the lead one step before is not zero
			bias=0.5-0.002*lead[i,inds[j]-1] #prob of scoring as function of lead (p.9 paper)
		else:
			bias=0.5
		if j<len(inds)-1: #if not the last event of the game
			fin=inds[j+1]
		else:
			fin=scope
		r_score=np.random.rand()
		s=0
		score=0
		for k in xrange(len(score_dist)):
			s+=score_dist[k]
			if r_score<s:
				score=k+1
				break
		r_who=np.random.rand()
		if r_who<bias: #decide which team gets the points
			lead[i,inds[j]:fin]=lead[i,inds[j]-1]+score
		else:
			lead[i,inds[j]:fin]=lead[i,inds[j]-1]-score
	fin_sign=np.sign(lead[i,scope-1]) #the sign of final lead shows who's the winner
	for l in reversed(xrange(len(inds))):
		if np.sign(lead[i,inds[l]])!=fin_sign:
			break
	t[i]=-1 if fin_sign==0 else inds[l+1]	
s=t[t>-1]
