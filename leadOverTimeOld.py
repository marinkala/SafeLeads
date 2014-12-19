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
#BJ_A=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
#BJ_B=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
#BJ_A[:,0]=LeadA[:,0]
#BJ_B[:,0]=LeadB[:,0]
#
#for t in xrange(scope):
#	BJ_A[:,t+1]=(LeadA[:,t+1]>(scope-t-1)**(0.5)+3)
#	BJ_B[:,t+1]=(LeadB[:,t+1]>(scope-t-1)**(0.5)+3)
#resA=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
#resB=np.zeros(games*(scope+1),dtype=np.int32).reshape((games,scope+1))
#resA[:,0]=LeadA[:,0]
#resB[:,0]=LeadB[:,0]
#resA[:,1:]=BJ_A[:,1:]==inLeadA[:,1:]
#resB[:,1:]=BJ_B[:,1:]==inLeadB[:,1:]
#accuracy=np.append(resA,resB).reshape(2*games,scope+1) #append the winner and loser
#
#tpA=(BJ_A[:,1:]==inLeadA[:,1:])&(inLeadA[:,1:]==1)
#tpB=(BJ_B[:,1:]==inLeadB[:,1:])&(inLeadB[:,1:]==1)
#tp=tpA+tpB #one of them is all False
#tnA=(BJ_A[:,1:]==inLeadA[:,1:])&(inLeadA[:,1:]==0)
#tnB=(BJ_B[:,1:]==inLeadB[:,1:])&(inLeadB[:,1:]==0)
#tn=np.append(tnA,tnB).reshape(2*games,scope)
#fpA=(BJ_A[:,1:]!=inLeadA[:,1:])&(inLeadA[:,1:]==0)
#fpB=(BJ_B[:,1:]!=inLeadB[:,1:])&(inLeadB[:,1:]==0)
#fp=fpA+fpB
#fnA=(BJ_A[:,1:]!=inLeadA[:,1:])&(inLeadA[:,1:]==1)
#fnB=(BJ_B[:,1:]!=inLeadB[:,1:])&(inLeadB[:,1:]==1)
#fn=np.append(fnA,fnB).reshape(2*games,scope)
#tp_rate=sum(sum(tp))/float(resA.size)
#tn_rate=sum(sum(tn))/float(2*resA.size)
#fp_rate=sum(sum(fp))/float(resA.size)
#fn_rate=sum(sum(fn))/float(2*resA.size)
#conf_arr=100*np.array([[tn_rate,fp_rate],[fn_rate,tp_rate]])

time=range(1,scope+1)
#accVec=sum(accuracy[:,1:])/float(2*games)#b/c 2 teams per game
#tpVec=sum(tp)/float(2*games)
#tnVec=sum(tn)/float(2*games)
#plt.plot(time,accVec,'b')
#plt.plot(time,tpVec,'g-')
#plt.plot(time,tnVec,'r--')
#plt.xlim(xmin=0,xmax=scope+2)
#plt.xlabel('Elapsed time, t (seconds)')
#plt.ylabel('Rate')
#plt.title(dir)
#plt.legend(('accuracy','true positive','true negative'),loc=6)
#plt.show()

leadSafeA=LeadA[:,1:]*inLeadA[:,1:]
leadSafeB=LeadB[:,1:]*inLeadB[:,1:]
leadSafe=leadSafeA +leadSafeB #one of them is all zeros
leadUnsafeA=LeadA[:,1:]*(inLeadA[:,1:]==0)
leadUnsafeB=LeadB[:,1:]*(inLeadB[:,1:]==0)
leadUnsafe=np.append(leadUnsafeA,leadUnsafeB).reshape(2*games,scope)
slead=[]
ulead=[]
slead_test=[]
ulead_test=[]
t=[]
ut=[]
t_test=[]
ut_test=[]
scount=0
ucount=0
for i in xrange(games):
	for j in xrange(scope): #or 2160,scope for last period
		if leadSafe[i,j]>0:
			if scount%3==0:
				slead_test.append(leadSafe[i,j])
				t_test.append(j+1)
			else:
				slead.append(leadSafe[i,j])
				t.append(j+1)
			scount+=1
		if leadUnsafe[2*i,j]>0: #no longer include negative leads - could not be safe
			if ucount%3==0:
				ulead_test.append(leadUnsafe[2*i,j])
				ut_test.append(j+1)
			else:
				ulead.append(leadUnsafe[2*i,j])
				ut.append(j+1)
			ucount+=1
		if leadUnsafe[2*i+1,j]>0: #no longer include negative leads - could not be safe
			if ucount%3==0:
				ulead_test.append(leadUnsafe[2*i+1,j])
				ut_test.append(j+1)
			else:
				ulead.append(leadUnsafe[2*i+1,j])
				ut.append(j+1)
			ucount+=1
lead=np.append(slead,ulead)
time=np.append(t,ut)
ys=np.ones(len(slead))
yu=np.zeros(len(ulead))
y=np.append(ys,yu)
m=lead.mean()
sd=lead.std()
leadz=(lead-m)/sd
mt=time.mean()
sdt=time.std()
tz=(time-mt)/sdt
X=np.vstack([time,lead]).T
Xz=np.vstack([tz,leadz]).T
lead_test=np.append(slead_test,ulead_test)
time_test=np.append(t_test,ut_test)
ys_test=np.ones(len(slead_test))
yu_test=np.zeros(len(ulead_test))
y_test=np.append(ys_test,yu_test)
m_test=lead_test.mean()
sd_test=lead_test.std()
leadz_test=(lead_test-m_test)/sd_test
mt_test=time_test.mean()
sdt_test=time_test.std()
tz_test=(time_test-mt_test)/sdt_test
X_test=np.vstack([time_test,lead_test]).T
Xz_test=np.vstack([tz_test,leadz_test]).T
train=np.zeros(len(X)*5).reshape(len(X),5)
test=np.zeros(len(X_test)*5).reshape(len(X_test),5)
train[:,:2]=X
train[:,2:4]=Xz
train[:,4]=y
test[:,:2]=X_test
test[:,2:4]=Xz_test
test[:,4]=y_test
train_df=pandas.DataFrame(train)
test_df=pandas.DataFrame(test)
#train_df.to_csv('timeLeadSafeTrainAll.csv')
#test_df.to_csv('timeLeadSafeTestAll.csv')


#scope_vec=scope*np.ones(scope)
#bj=(scope_vec-time)**0.5+3
#heatmap, xedges, yedges = np.histogram2d(t, lead, [2880,60],normed=True)
#plt.imshow(heatmap.T, aspect='auto',origin='lower')
#plt.scatter(t,lead)
#plt.plot(time,bj,'r--',linewidth=2.0)
#plt.ylim(ymin=0,ymax=59)
#plt.xlim(xmin=0,xmax=scope+2)
#plt.xlabel('Elapsed time, t (seconds)')
#plt.ylabel('Lead')
#plt.title(dir)
#plt.show()