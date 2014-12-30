import pandas
import numpy as np
import matplotlib.pyplot as plt
import UnbiasedRW as rw

def getData(sport):
	folder='/Users/Ish/Documents/SafeLeads/Results/'
	path=folder+'/'+sport+'_res'

	data=pandas.read_csv(path+'/'+sport+'_all_lead.csv', parse_dates=False,\
	usecols=['SEASON','GAME_CODE','TEAM_ID','event_time','POINTS'])
	return data
	
def getBias(data):
	grouped=data.groupby(['SEASON','GAME_CODE'])
	games=len(grouped)
	qs=np.zeros(games)
	i=0
	for name, group in grouped: #for each game
		teams=group.TEAM_ID
		frac=len(teams[teams==teams.iloc[0]])/float(len(teams))
		#num of events won by first team/ num of all events
		if frac>0.5:
			qs[i]=frac
		else:
			qs[i]=1-frac
		i+=1
	bias=qs.mean()
	return bias	
	
def Lead(data, sport):
	if (sport=='NBA'):
		scope=2880
	else: 
		scope=3600
	grouped=data.groupby(['SEASON','GAME_CODE'])
	games=len(grouped)

	#Translate the event data into the leads for each team 
	lead=np.zeros((games,scope),dtype=np.int32)
	gameLead=np.zeros((games, 2))
	i=0
	for name, group in grouped: #for each game
		thisGameEvents=(group.event_time-1).tolist() #times of events for this game -1 for 0-indexing
		thisGamePoints=group.POINTS.tolist()
		events=np.zeros(scope)
		starter=group.TEAM_ID.iloc[0] #the first team to score get +
		for j in xrange(len(thisGameEvents)): #for each event in this game
			if group.TEAM_ID.iloc[j]!=starter:
				isStarter=-1
			else:
				isStarter=1
			events[thisGameEvents[j]]=thisGamePoints[j]*isStarter
		lead[i]=np.cumsum(events)
		#gameLead[i][0]=group.GAME_CODE.unique()
		#gameLead[i][1]=lead[i][-1]
		#create a list of games with corresponding last lead here!
		i+=1
	#pandas.DataFrame(gameLead).to_csv(sport+'gameLead.csv')
	return lead

def inLead(lead):	
	#Which team is in the lead at any given time
	games=len(lead)
	scope=len(lead[0])
	inLead=np.zeros((games,scope)) 
	inLead[lead>0]=1 #team who scored first is in the lead
	inLead[lead<0]=-1
	return inLead
	
def lastChangeMessy(inLead):
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
	return tr #this is for assign safety function below

def lastChange(inLead):
	tr=lastChangeMessy(inLead)
	s=tr[tr>-1]
	s=s+1
	return s

def assignSafety(lastLeadChange, sport): 
	games=len(lastLeadChange)
	if (sport=='NBA'):
		scope=2880
	else: 
		scope=3600
	safe=np.zeros((games,scope))
	for i in xrange(games):
		if lastLeadChange[i]!=-1:
			safe[i,lastLeadChange[i]:]=1
	return safe

def  getZ(lead,safe,sport):
	games=len(lead)
	scope,scores=rw.getScope(sport)
	p=scores/scope
	D=1/(4*p)
	z_tuples=np.zeros((games*scope,3))
	count=0
	for i in xrange(games):
		for j in xrange(scope):
			#z=abs(lead[i][j])/((4*D*(scope-j-1))**0.5)
			z_tuples[count,0]=abs(lead[i,j])#z
			z_tuples[count,1]=j+1#safe[i,j]
			z_tuples[count,2]=safe[i,j]
			count+=1
	return z_tuples

def numChanges(inLead, lead):
	games=len(inLead)
	scope=len(inLead[0])
	changes=-1*np.ones(games)
	for i in xrange(games):
		thisGameChanges=[]
		for j in xrange(scope-1):
			if (inLead[i][j]!=inLead[i][j+1]) & (lead[i][j]!=0):
			#w/out (inLead[i][j+1]!=0) counts changes from and to 0, including 1st score
			#w/ (inLead[i][j+1]!=0) doesn't count switching to 0, but still has 1st score
				thisGameChanges.append(j+1)
		changes[i]=len(thisGameChanges)#-1 #to discount the first scoring event
	#changes.tofile(sport+'numLeadChangesZeros.txt',sep=',')
	return changes
	
def firstChange(inLead):
	games=len(inLead)
	scope=len(inLead[0])
	firstCh=-1*np.ones(games)
	for i in xrange(games):
		thisGameChanges=[]
		for j in xrange(scope-1):
			if (inLead[i][j]!=inLead[i][j+1]) & (inLead[i][j+1]!=0):
			#w/out (inLead[i][j+1]!=0) counts changes from and to 0, including 1st score
			#w/ (inLead[i][j+1]!=0) doesn't count switching to 0, but still has 1st score
				thisGameChanges.append(j+1)
		if len(thisGameChanges)>1:		
			firstCh[i]=thisGameChanges[1]#to drop the first scoring event
		elif inLead[i][-1]==0:#one-team lead games that ends in a tie
			firstCh[i]=0
	return firstCh
	
def maxLeadTime(lead):
	games=len(lead)
	m=np.max(lead,axis=1)
	t=np.zeros(games)
	for i in xrange(games):
		t[i]=np.where(lead[i]==m[i])[0][0]+1 #game time starts from 1, not 0
	return m,t
	
def prepLeadHeatMap(lead):
	scope=len(lead[0])
	games=len(lead)
	flatLead=lead.flatten()
	seconds=range(1, scope+1)
	flatT=np.tile(seconds,games)
	return flatT, abs(flatLead)
	
def sdLead(lead):
	scope=len(lead[0])
	posLead=abs(lead)
	negLead=-posLead
	doubLead=np.concatenate((posLead,negLead),axis=0)
	sd=np.std(doubLead,axis=0)
	per75=np.percentile(doubLead,75,axis=0)
	per90=np.percentile(doubLead,90,axis=0)
	x=range(1,scope+1)
	y=np.sqrt(x)/2.7
	plt.plot(x,sd, 'b',linewidth=2,label=r'Empirical: $\sigma$')
	plt.plot(x,per75, 'g',linewidth=2,label=r'Empirical: $75^{th} Percentile$')
	plt.plot(x,per90, 'y',linewidth=2,label=r'Empirical: $90^{th} Percentile$')
	plt.plot(x,y,'r', linewidth=2,label=r'Theoretical: $y\propto \sqrt{t}$')
	plt.xlim(xmin=0,xmax=scope)
	plt.xlabel('Elapsed time, s')
	plt.ylabel('Lead Size Dispersion')
	plt.legend(loc=(0.03,0.66))
	leg=plt.gca().get_legend()
	leg.draw_frame(False)
	plt.show()