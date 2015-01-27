import numpy as np
import matplotlib.pyplot as plt
import leadOverTimeLatest as lt
import SimpleModel as rw
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

def AveNumLeadChanges(sport):
	if sport=='NBA':
		N=91.99
	elif sport=='NHL':
		N=3.81
	elif sport=='CFB':
		N=8.28
	elif sport=='NFL':
		N=7.34
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	hcorr,b=getNumFreq(lead)
	maxc=b[-1]
	rw_lead=rw.Lead(sport)
	hcorr1,b1=getNumFreq(rw_lead)
	plt.scatter(b[:b[-1]],hcorr,facecolors='none', edgecolors='red',marker='s',label=sport+' data')
	plt.scatter(b1[:b1[-1]], hcorr1, facecolors='none', edgecolors='blue', marker='o', label='simulation')
	#sqrt{2 / ( pi*N) }*exp(-(m^2) / (2N))
	x=np.arange(0,maxc+0.1, 0.1)
	y=((2/(np.pi*N))**0.5)*np.exp(-(x**2)/(2*N))
	plt.plot(x,y, c='black', linewidth=2, label='theory')
	plt.xlim(xmin=0,xmax=maxc)
	plt.ylim(ymin=0)
	plt.xlabel('Number of lead changes')
	plt.ylabel('Relative frequency')
	plt.legend()
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
	rw_lead=rw.Lead(sport)
	rw_z, rw_q=getSafeAvg(rw_lead, sport)
	BJsafe=lt.BJ(lead)
	BJz_tuples=lt.getZ(lead, BJsafe, sport)
	BJdf=pd.DataFrame(BJz_tuples)
	BJz,BJq=binAverage(BJdf)

	plt.scatter(z,ave_q, color='red', marker='s', label=sport+' data')
	plt.plot(rw_z,rw_q, color='black', linewidth=2.5, label='theory (unbiased rw)')
	plt.plot(BJz, BJq, 'b--', linewidth=2.5,label='Bill James\' rule')
	plt.legend()
	plt.xlim(0,2.5)
	plt.ylim(0,1)
	plt.xlabel('Effective lead, z')
	plt.ylabel('Probability that effective lead is safe')
	plt.show()

