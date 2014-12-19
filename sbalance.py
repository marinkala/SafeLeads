import pandas
import numpy
from matplotlib import pyplot as plt
import sys

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_res'

data=pandas.DataFrame.from_csv(path+'/'+dir+'_synthData.csv', \
	parse_dates=False)

#function to get cumulative points
def accum(group):
    n=len(group)
    y=group
    for i in xrange(n-1):
        y.iloc[i+1]=sum(group[i:i+2])
    return y

#function to fill the zeros with the highest previous score
def fill(group): 
    n=len(group)
    y=group
    for i in xrange(n):
        if (group.iloc[i]==0) & (i!=0):
            y.iloc[i]=max(group[0:i])
    return y

#function to shift the lead - to show the lead by the time event occurs
def shift(group):
	n=len(group)
	y=group
	y[1:n]=group[0:n-1]
	y.iloc[0]=0
	return y
	
def switch(x):
	if ((x['shift_lead']>0) & (x['double_shift_lead']<0)) | \
		((x['shift_lead']<0) & (x['double_shift_lead']>0)) | (x['shift_lead']==0):
		result=1
	else:
		result=0
	return result

data=data.sort(['GAME_CODE','TEAM_ID'])
grouped=data.groupby(['GAME_CODE','TEAM_ID'])
data['cum_points']=grouped.POINTS.apply(accum)
data=data.sort(['GAME_CODE','event_time'])

#to get separate cum_points for starter and followers
game_gr=data.groupby('GAME_CODE')
new_data=pandas.DataFrame()

for name, group in game_gr:
    n=len(group.TEAM_ID)#get number of events whithin the game
    s=group.TEAM_ID.iloc[0]#get the team code of the team that scores first
    group=group.sort(['TEAM_ID','event_time'])
    order=group.TEAM_ID.iloc[0]#get the team code of the team first on the list
    team_gr=group.groupby('TEAM_ID')
    starter=n*[0]
    follower=n*[0]
    for name1,group1 in team_gr:
        if group1.TEAM_ID.iloc[0]==order:
            starter[0:len(group1.TEAM_ID)]=group1.cum_points
        else:
            follower[n-len(group1.TEAM_ID):n]=group1.cum_points
    if order==s:
        group['starter']=starter
        group['follower']=follower
    else:
        group['starter']=follower
        group['follower']=starter
    new_data=new_data.append(group)

new_data=new_data.sort(['GAME_CODE','event_time']).reset_index(drop=True)

grouped=new_data.groupby(['GAME_CODE'])
new_data['start_fill']=grouped.starter.apply(fill)
new_data['foll_fill']=grouped.follower.apply(fill)
new_data['lead']=new_data['start_fill']-new_data['foll_fill']

#shift the lead so it reflects the lead BEFORE the current event
group_sft=new_data.groupby('GAME_CODE')
new_data['shift_lead']=group_sft.lead.apply(shift)
new_data['double_shift_lead']=group_sft.shift_lead.apply(shift)
new_data['switch']=new_data.apply(switch,axis=1)
del new_data['double_shift_lead']

grouped=new_data.groupby('GAME_CODE')
l_change=pandas.Series()
for name, group in grouped:
    n=len(group)
    inds=group.index[group.switch==1]
    end=inds.values[0]+n-1
    num_chunks=len(inds.values)
    game_change=pandas.Series()
    for i in xrange(num_chunks):
        if i==num_chunks-1: #last chunk
            chunk=group.ix[inds.values[i]:end]
        else:
            chunk=group.ix[inds.values[i]:inds.values[i+1]-1]
        if (chunk.shift_lead.iloc[0]<0) | ((chunk.shift_lead.iloc[0]==0) & (chunk.lead.iloc[0]<0)):
            chunk_lead_change=chunk.shift_lead-chunk.lead
        else:
            chunk_lead_change=chunk.lead-chunk.shift_lead
        game_change=game_change.append(chunk_lead_change)
    l_change=l_change.append(game_change)
new_data['lead_change']=l_change

new_data['abs_shift_lead']=abs(new_data.shift_lead)
lim=max(new_data.abs_shift_lead)
lead_prob=pandas.Series(data=0.5,index=xrange(-lim,lim+1))

for i in xrange(1,lim+1):
    if len(new_data[new_data.abs_shift_lead==i])>0:
        lead_prob[i]=len(new_data[(new_data.abs_shift_lead==i)&(new_data.lead_change>0)])/\
float(len(new_data[new_data.abs_shift_lead==i]))
        lead_prob[-i]=1-lead_prob[i]


[b,a]=numpy.polyfit(lead_prob.index,lead_prob,1)
x = numpy.arange(-lim,lim, 10)
y = b*x+a
plt.scatter(lead_prob.index,lead_prob)
plt.plot(x, y, 'r-')
plt.ylim(ymin=0,ymax=1)
plt.xlabel('Lead size, L')
plt.ylabel('Pr(scoring next event)')
plt.title('Synthetic '+dir)
plt.show()