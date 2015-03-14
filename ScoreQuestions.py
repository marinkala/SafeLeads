def getScores(events):
	games=len(events)
	scope=len(events[0])
	winner=[]
	loser=[]
	for i in xrange(games):
		a=sum(events[i][events[i]>0])
		b=abs(sum(events[i][events[i]<0]))
		if a>b:
			winner.append(a)
			loser.append(b)
		else:
			winner.append(b)
			loser.append(a)
	return winner, loser

def sumScores(events):
	games=len(events)
	scope=len(events[0])
	scores=[]
	for i in xrange(games):
		a=sum(events[i][events[i]>0])
		b=abs(sum(events[i][events[i]<0]))
		scores.append(a+b)
	return scores

def rmsDiff(winner, loser):
	rms=[]
	for i in xrange (len(winner)):
		rms.append(((winner[i]**2+loser[i]**2)/2)**0.5)
	return rms