import pandas
import numpy as np
import matplotlib.pyplot as plt
import sys

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_res'

if (dir=='NBA'):
	scope=2880
else: 
	scope=3600

data=pandas.DataFrame.from_csv(path+'/'+dir+'_all_lead.csv', \
	parse_dates=False)

grouped=data.groupby(['SEASON','GAME_CODE'])
games=len(grouped)
inLeadA=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1)) 
#+1 for the game code
inLeadB=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
LeadA=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
LeadB=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))

count=0
for name, group in grouped:#for each game
	num_events=len(group)

	inLA=np.zeros(scope,dtype=np.int32) #A is always the team that scored first
	inLB=np.zeros(scope,dtype=np.int32) 
	lA=np.zeros(scope,dtype=np.int32)
	lB=np.zeros(scope,dtype=np.int32)
	#all seconds upto the first event will have lead of 0
	#start from the second event - since we go backwards to previous
	#teams=set(group.TEAM_ID.unique())
	starter=group.TEAM_ID.iloc[0] #the first in the set - the starter
	winner=0
	crossed=0
	for i in reversed(xrange(num_events)): #go from last event backwards
		start=group.event_time.iloc[i]-1
		if i<num_events-1: #not the last event for that game
			fin=group.event_time.iloc[i+1]-1
		else: #last event of the game
			fin=scope+1
			if group.lead.iloc[i]>0:
				winner=starter
			#else:
				#winner=teams.pop() #the follower
		if winner==starter:
			if (not crossed) & (group.lead.iloc[i]>0): #starter in the lead 
				inLA[start:fin]=1
			else:
				crossed=1
		else:
			if (not crossed) & (group.lead.iloc[i]<0): #follower in the lead 
				inLB[start:fin]=1
			else:
				crossed=1
		lA[start:fin]=group.lead.iloc[i]
		lB[start:fin]=-group.lead.iloc[i]
		#otherwise inLead and Lead will remain zero
	inLeadA[count,0]=group.GAME_CODE.iloc[0]	
	inLeadA[count,1:]=inLA
	inLeadB[count,0]=group.GAME_CODE.iloc[0]	
	inLeadB[count,1:]=inLB	
	LeadA[count,0]=group.GAME_CODE.iloc[0]	
	LeadA[count,1:]=lA
	LeadB[count,0]=group.GAME_CODE.iloc[0]	
	LeadB[count,1:]=lB
	count+=1

#leadSafeA=LeadA[:,1:]*inLeadA[:,1:]
#leadSafeB=LeadB[:,1:]*inLeadB[:,1:]
#leadSafe=leadSafeA +leadSafeB #one of them is all zeros
#leadUnsafeA=LeadA[:,1:]*(inLeadA[:,1:]==0)
#leadUnsafeB=LeadB[:,1:]*(inLeadB[:,1:]==0)
#leadUnsafe=np.append(leadUnsafeA,leadUnsafeB).reshape(2*games,scope)
#slead=[]
#ulead=[]
#t=[]
#ut=[]
#scount=0
#ucount=0
#for i in xrange(games):
#	for j in xrange(scope): #or 2160,scope for last period
#		if leadSafe[i,j]>0:
#			slead.append(leadSafe[i,j])
#			t.append(j+1)
#			scount+=1
#		if leadUnsafe[2*i,j]>0: #no longer include negative leads - could not be safe
#			ulead.append(leadUnsafe[2*i,j])
#			ut.append(j+1)
#			ucount+=1
#		if leadUnsafe[2*i+1,j]>0: #no longer include negative leads - could not be safe
#			ulead.append(leadUnsafe[2*i+1,j])
#			ut.append(j+1)
#			ucount+=1
#lead=np.append(slead,ulead)
#time=np.append(t,ut)
#ys=np.ones(len(slead))
#yu=np.zeros(len(ulead))
#y=np.append(ys,yu)
#m=lead.mean()
#sd=lead.std()
#leadz=(lead-m)/sd
#mt=time.mean()
#sdt=time.std()
#tz=(time-mt)/sdt
#X=np.vstack([time,lead]).T
#Xz=np.vstack([tz,leadz]).T
#data=np.zeros(len(X)*5).reshape(len(X),5)
#data[:,:2]=X
#data[:,2:4]=Xz
#data[:,4]=y
#df=pandas.DataFrame(data)
#df.to_csv(path+'/'+'timeLeadSafeAll.csv')
