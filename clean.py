import pandas
import os.path
import sys

dir=sys.argv[1]
folder='C:\Users\Ish\Desktop\Aaron\\'
path=folder+'/'+dir+'_data'

if (dir=='NBA') | (dir=='NHL'):
	term='PERIOD'
else:
	term='QUARTER'
if (dir=='NHL'):
	time='TIME_IN'
else:
	time='TIME_LEFT'

df=pandas.DataFrame()
for filename in os.listdir(path):
	data=pandas.DataFrame.from_csv(path+'/'+filename, index_col=None, parse_dates=False)
	year=int(filename.rstrip('.CSV')[-4:])
	
	#remove overtime events, but not games
	if dir=='NBA':
		data=data[data[term]<5]
	if dir=='NHL':
		data=data[data[term]<4]
	else: #CFB & NFL
		data=data[data[term]<5]
	
	#combine events that are at the same time
	grouped=data.groupby(['GAME_CODE','TEAM_ID', term,time])
	data=grouped.POINTS.aggregate(sum).reset_index()
	data['SEASON']=year

	#remove games with both teams scoring at once
#	grouped=data.groupby(['GAME_CODE',term,time])
#	data['double']=grouped.POINTS.transform(lambda x: len(x))
#	games_double=data.GAME_CODE[data.double==2]
#	data['excl']=data.GAME_CODE.apply(lambda x: 1 if x in games_double.values else 0)
#	data=data[data.excl==0]
	df=df.append(data)

df=df[['SEASON','GAME_CODE','TEAM_ID',term,time,'POINTS']].reset_index(drop=True)
df.to_csv('C:\Users\Ish\Desktop\Aaron\\'+'/'+dir+'_res'+'/'+dir+'_all_clean.csv')