import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import leadOverTimeLatest as lt
import SimpleModel as sm
import UnbiasedRW as rw
import probLastLeadChangeArcs as arcs
import pandas as pd

def getNumFreq(lead):
	inLead=lt.inLead(lead)
	changes=lt.numChanges(inLead, lead)
	print np.mean(changes)
	h,b=np.histogram(changes, max(changes)-min(changes))
	hcorr=h/float(len(changes))
	return hcorr,b

def getLastLeadFreq(lead, bins):
	inLead=lt.inLead(lead)
	s=lt.lastChange(inLead)
	h,b=np.histogram(s, bins)
	binw=arcs.getBinWidth(bins)
	hcorr=h/(binw*len(s))
	return hcorr, b

def binAverage(df):
	step=0.05
	bins=np.arange(0,2.5+step,step)
	df[2]=np.digitize(df[0],bins) #assign a bin number to each tuple
	gr=df[1].groupby(df[2]) #not all the bin numbers are present!
	ave_q=gr.mean()
	bin_nums=np.sort(df[2].unique())
	z1=[bins[i-1] for i in bin_nums]
	return z1, ave_q

def getSafeAvg(lead, sport):
	inLead=lt.inLead(lead)
	lastChange=lt.lastChangeMessy(inLead)
	safe=lt.assignSafety(lastChange, sport)
	z_tuples=lt.getZ(lead, safe, sport)
	df=pd.DataFrame(z_tuples)
	z1,ave_q=binAverage(df)
	return z1,ave_q


def calcTertiles(lead):
	lastLead=abs(lead[:,-1])
	top1=np.percentile(lastLead,33)
	top2=np.percentile(lastLead, 67)
	maxLead=max(lastLead)
	return top1, top2, maxLead

def getTertiles(lead, top1, top2):
	lastLead=abs(lead[:,-1])
	lead1=lead[lastLead<=top1]
	lead2=lead[(lastLead>top1) & (lastLead<=top2)]
	lead3=lead[lastLead>top2]
	return lead1, lead2, lead3

def movingaverage(interval, window_size):
    window= np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def NumLeadChanges(sport):
	scope,N=rw.getScope(sport)
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	hcorr,b=getNumFreq(lead)
	maxc=b[-1]
	rw_lead=rw.Lead(sport)
	hcorr1,b1=getNumFreq(rw_lead)
	#(b[:b[-1]]).tofile('../Results/'+sport+'numLeadChangesX.csv', sep=',')
	#hcorr.tofile('../Results/'+sport+'numLeadChangesY.csv', sep=',')

	fontSize=18
	ax=plt.gca()
	ax.tick_params(labelsize=fontSize)
	plt.plot(b[:b[-1]],hcorr,'r^-',lw=2, ms=8,label=sport+' data')
	plt.plot(b1[:b1[-1]], hcorr1, 'bo-',lw=2, ms=8, label='Poisson process')
	#sqrt{2 / ( pi*N) }*exp(-(m^2) / (2N))
	x=np.arange(0,maxc+0.1, 0.1)
	y=((2/(np.pi*N))**0.5)*np.exp(-(x**2)/(2*N))
	plt.plot(x,y, c='black', linewidth=2, label='Eq.(3)')
	plt.xlim(xmin=0,xmax=maxc)
	plt.ylim(ymin=0,ymax=0.5)
	plt.xlabel('Number of lead changes', fontsize=fontSize)
	plt.ylabel('Relative frequency', fontsize=fontSize)
	plt.legend(prop={'size':fontSize})
	plt.show()

def NumLeadChangesBias(sport):
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	top1, top2,maxLead=calcTertiles(lead)
	lead1,lead2,lead3=getTertiles(lead, top1, top2)
	hcorr1, b1=getNumFreq(lead1)
	hcorr2, b2=getNumFreq(lead2)
	hcorr3, b3=getNumFreq(lead3)
	maxc=b1[-1]
	plt.scatter(b1[:b1[-1]],hcorr1,facecolors='none', edgecolors='red',marker='s',\
label=sport+' data, final lead diff: 0-'+str(int(top1)))
	plt.scatter(b2[:b2[-1]], hcorr2, facecolors='none', edgecolors='blue', marker='o', \
label=sport+' data, final lead diff: '+str(int(top1))+"-"+str(int(top2)))
	plt.scatter(b3[:b3[-1]],hcorr3,facecolors='none', edgecolors='green',marker='D',\
label=sport+' data, final lead diff: '+str(int(top2))+'-'+str(int(maxLead)))
	plt.xlim(xmin=0, xmax=maxc)
	plt.ylim(ymin=0)
	plt.xlabel('Number of lead changes')
	plt.ylabel('Relative frequency')
	plt.legend()
	plt.show()

def LastLeadChangeBias(sport):
	if sport=='NBA':
		scope=2880
		bins=arcs.NBAbins()
	else:
		scope=3600
		if sport=='NHL':
			bins=arcs.NHLbins()
		else:
			bins=arcs.NFLbins()
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	top1, top2,maxLead=calcTertiles(lead)
	lead1,lead2,lead3=getTertiles(lead, top1, top2)
	hcorr1, b1=getLastLeadFreq(lead1,bins)
	hcorr2, b2=getLastLeadFreq(lead2,bins)
	hcorr3, b3=getLastLeadFreq(lead3,bins)
	plt.scatter(b1[:len(b1)-1],hcorr1,facecolors='none', edgecolors='red',marker='s',\
label=sport+' data, final lead diff: 0-'+str(int(top1)))
	plt.scatter(b2[:len(b2)-1], hcorr2, facecolors='none', edgecolors='blue', marker='o', \
label=sport+' data, final lead diff: '+str(int(top1))+"-"+str(int(top2)))
	plt.scatter(b3[:len(b3)-1],hcorr3,facecolors='none', edgecolors='green',marker='D',\
label=sport+' data, final lead diff: '+str(int(top2))+'-'+str(int(maxLead)))	
	plt.xlim(xmin=0, xmax=scope)
	plt.ylim(ymin=0, ymax=0.0025)
	plt.xlabel('Clock time, seconds')
	plt.ylabel('Probability of last lead change')
	plt.legend()
	plt.show()

def ProbLeadSafe(sport):
	data=lt.getData(sport)
	lead=lt.Lead(data,sport)
	z, ave_q=getSafeAvg(lead, sport)
	sm_lead=sm.Lead(sport)
	sm_z, sm_q=getSafeAvg(sm_lead, sport)
	#BJsafe=lt.BJ(lead)
	#BJz_tuples=lt.getZ(lead, BJsafe, sport)
	#BJdf=pd.DataFrame(BJz_tuples)
	#BJz,BJq=binAverage(BJdf)

	plt.scatter(z,ave_q, color='red', marker='s', label=sport+' data')
	plt.plot(sm_z,sm_q, color='black', linewidth=2.5, label='theory (unbiased rw)')
	#plt.plot(BJz, BJq, 'b--', linewidth=2.5,label='Bill James\' rule')
	plt.legend()
	plt.xlim(0,2)
	plt.ylim(0,1)
	plt.xlabel('Effective lead, z')
	plt.ylabel('Probability that effective lead is safe')
	plt.show()

def PropInLead(sport):
	#portion of time first team to score is in the lead

	data=lt.getData(sport)
	lead=lt.Lead(data,sport)
	inLead=lt.inLead(lead)
	rands=np.random.rand(len(inLead))
	mult=-1+2*(rands<0.5)
	matr=(np.tile(mult,(len(inLead[0]),1))).T
	rand_inLead=np.multiply(matr, inLead)

	props=np.sum(rand_inLead<0, axis=1)

	sm_lead=sm.Lead(sport)
	sm_inLead=sm.inLead(sm_lead)
	rands=np.random.rand(len(sm_inLead))
	mult=-1+2*(rands<0.5)
	matr=(np.tile(mult,(len(sm_inLead[0]),1))).T
	sm_randInLead=np.multiply(matr,sm_inLead)
	sm_props=np.sum(sm_randInLead<0,axis=1)

	rw_lead=rw.Lead(sport)
	rw_inLead=rw.inLead(rw_lead)
	rands=np.random.rand(len(rw_inLead))
	mult=-1+2*(rands<0.5)
	matr=(np.tile(mult,(len(rw_inLead[0]),1))).T
	rw_randInLead=np.multiply(matr, rw_inLead)
	rw_props=np.sum(rw_randInLead<0,axis=1)

	if sport=='NBA':
		scope=2880
		bins=arcs.NBAbins()
	else:
		scope=3600
		if sport=='NHL':
			bins=arcs.NHLbins()
		else:
			bins=arcs.NFLbins()

	binw=arcs.getBinWidth(bins)
	fontSize=18

	ax=plt.gca()
	ax.tick_params(labelsize=fontSize)
	h,b=np.histogram(props, bins)
	hcorr=h/(binw*len(props))
	plt.scatter(b[:len(bins)-1], hcorr, c='blue',marker='o',label=sport+' games') 

	hr,br=np.histogram(sm_props,bins)
	hrcorr=hr/(binw*len(sm_props))
	plt.plot(br[:len(bins)-1],hrcorr,color='DarkTurquoise', linewidth=2,label='Inhomogeneous Poisson process')
	#Unbiased rw
	#rwstep=20.0
	#rwbins=scope/rwstep
	#hw,bw=np.histogram(rw_props,rwbins)
	#hwcorr=hw/(rwstep*len(rw_props))
	#plt.plot(bw[:rwbins],hwcorr,color='DarkSalmon', linewidth=2,label='Homogeneous Poisson process')
	#arcsine law
	x=np.array(range(scope)) 
	y=1/(np.pi*(x*(scope+1-x))**(0.5))
	plt.plot(x,y,color='FireBrick',linewidth=2,label='Arcsine law')
	plt.xlim(xmin=0,xmax=scope)
	plt.ylim(ymin=0,ymax=0.0027)
	plt.legend(prop={'size':fontSize})
	plt.xlabel('Number of seconds a team is in the lead', fontsize=fontSize)
	plt.ylabel('Relative frequency', fontsize=fontSize)
	plt.subplots_adjust(left=0.16, right=0.95, top=0.95, bottom=0.13)
	#plt.savefig(sport+'varBinnedUpdate.pdf')
	#plt.close()
	plt.show()

def plotWScoringRate(sport):
	if sport=='NBA':
		scope=2880
		seasons='2002-2010'
		bins=arcs.NBAbins()
	else:
		scope=3600
		seasons='2000-2009'
		if sport=='NHL':
			bins=arcs.NHLbins()
		elif sport=='CFB':
			bins=arcs.NFLbins()
		elif sport=='NFL':
			bins=arcs.NFLbins()

	binw=arcs.getBinWidth(bins)
	
	step=120.0
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	inLead=lt.inLead(lead)
	s=lt.lastChange(inLead)
	#m,s=lt.maxLeadTime(lead)
	'''rw_lead=rwk.Lead(sport)
	rw_inLead=rwk.inLead(rw_lead)
	rw=rwk.lastChange(rw_inLead)'''
	sm_lead=sm.Lead(sport)
	sm_inLead=sm.inLead(sm_lead)
	sr=sm.lastChange(sm_inLead)
	#msr,sr=lt.maxLeadTime(sm_lead)

	ev_prob=pd.DataFrame.from_csv('/Users/Ish/Documents/SafeLeads/Results/'+sport+'_res/'+sport+'_eventProb.csv',\
header=None)

	fontSize=18
	window=10
	#f, (ax1, ax2) = plt.subplots(2, sharex=True)
	f=plt.figure()
	gs=gridspec.GridSpec(2,1,height_ratios=[2,3]) #1 used to be 3
	ax1=plt.subplot(gs[0,:])
	ax2=plt.subplot(gs[1:,:], sharex=ax1)
	smoothEvProb=movingaverage(ev_prob[1],window)
	avg=np.mean(smoothEvProb)
	#y_formatter = matplotlib.ticker.ScalarFormatter(useOffset=-100)
	#ax1.yaxis.set_major_formatter(y_formatter)
	ax1.plot(smoothEvProb, linewidth=1.3)
	ax1.hlines(avg, 0,scope, colors='red', linewidth=2)
	yticks = ax1.yaxis.get_major_ticks()
	yticks[0].label1.set_visible(False)
	ax1.set_ylim(ymin=0,ymax=max(smoothEvProb)+0.005)
	ax1.set_ylabel('Pr(scoring event)',fontsize=fontSize, labelpad=25)#25 for NBA
	ax1.tick_params(labelsize=fontSize)


	ax2.tick_params(labelsize=fontSize)

	h,b=np.histogram(s, bins)
	hcorr=h/(binw*len(s))
	ax2.scatter(b[:len(bins)-1], hcorr, c='blue',marker='o',label=sport+' games') 
	hr,br=np.histogram(sr,bins)
	hrcorr=hr/(binw*len(sr))
	ax2.plot(br[:len(bins)-1],hrcorr,color='DarkTurquoise',linewidth=2,label='Inhomogeneous Poisson process')
	#ubiased RW
	'''rwstep=20.0
	rwbins=scope/rwstep
	h,b=np.histogram(rw, rwbins)
	hcorr=h/(rwstep*len(rw))
	plt.plot(b[:rwbins], hcorr, c='purple',linewidth=2.5,label='Homogenous Poisson process') '''
	x=np.array(range(scope)) #arcsine law
	y=1/(np.pi*(x*(scope+1-x))**(0.5))
	ax2.plot(x,y,color='FireBrick',linewidth=2,label='Arcsine law')
	ax2.set_xlim(xmin=0,xmax=scope)
	ax2.set_ylim(ymin=0,ymax=0.0027)
	ax2.legend(prop={'size':fontSize})
	ax2.set_xlabel('Game clock time, t (seconds)', fontsize=fontSize)
	ax2.set_ylabel('Pr(last lead change)', fontsize=fontSize)
	f.subplots_adjust(left=0.16, right=0.95, top=0.95, bottom=0.11, hspace=0.00001) #16,13
	# Fine-tune figure; make subplots close to each other and hide x ticks for
	# all but bottom plot.
	plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)
	plt.show()