import UnbiasedRW as rwk
import SimpleModel as sm
import leadOverTimeLatest as lt
import numpy as np
import matplotlib.pyplot as plt

def NBAbins():
	small_step=3
	big_step=20
	bins1=np.arange(1,50,small_step)
	bins2=np.arange(bins1[-1]+big_step,700,big_step)
	bins3=np.arange(bins2[-1]+small_step,740,small_step)
	bins4=np.arange(bins3[-1]+big_step,1420,big_step)
	bins5=np.arange(bins4[-1]+small_step,1460,small_step)
	bins6=np.arange(bins5[-1]+big_step,2140,big_step)
	bins7=np.arange(bins6[-1]+small_step,2180,small_step)
	bins8=np.arange(bins7[-1]+big_step,2850,big_step)
	bins9=np.arange(bins8[-1]+small_step,2881,small_step)
	bins=np.concatenate((bins1,bins2,bins3,bins4,bins5,bins6,bins7,bins8,bins9))
	return bins
	
def NFLbins():
	small_step=3
	big_step=20
	#bins1=np.arange(1,250,small_step)
	bins2=np.arange(1,880,big_step)
	bins3=np.arange(bins2[-1]+small_step,920,small_step)
	bins4=np.arange(bins3[-1]+big_step,1750,big_step)
	bins5=np.arange(bins4[-1]+small_step,1850,small_step)
	bins6=np.arange(bins5[-1]+big_step,2680,big_step)
	bins7=np.arange(bins6[-1]+small_step,2720,small_step)
	bins8=np.arange(bins7[-1]+big_step,3570,big_step)
	bins9=np.arange(bins8[-1]+small_step,3601,small_step)
	bins=np.concatenate((bins2,bins3,bins4,bins5,bins6,bins7,bins8,bins9))
	return bins
	
def NHLbins():
	small_step=3
	big_step=20
	#bins1=np.arange(1,250,small_step)
	bins2=np.arange(1,1180,big_step)
	bins3=np.arange(bins2[-1]+small_step,1220,small_step)
	bins4=np.arange(bins3[-1]+big_step,2380,big_step)
	bins5=np.arange(bins4[-1]+small_step,2420,small_step)
	bins6=np.arange(bins5[-1]+big_step,3570,big_step)
	bins7=np.arange(bins6[-1]+small_step,3601,small_step)
	bins=np.concatenate((bins2,bins3,bins4,bins5,bins6,bins7))
	return bins
	
def getBinWidth(bins):
	binw=np.zeros(len(bins)-1)
	for i in xrange(len(bins)-1):
		binw[i]=bins[i+1]-bins[i]
	return binw

def plotBathtub(sport):
	if sport=='NBA':
		scope=2880
		seasons='2002-2010'
		bins=NBAbins()
	else:
		scope=3600
		seasons='2000-2009'
		if sport=='NHL':
			bins=NHLbins()
		elif sport=='CFB':
			bins=NFLbins()
		elif sport=='NFL':
			bins=NFLbins()

	binw=getBinWidth(bins)
	
	step=120.0
	data=lt.getData(sport)
	lead=lt.Lead(data, sport)
	#inLead=lt.inLead(lead)
	#s=lt.lastChange(inLead)
	m,s=lt.maxLeadTime(lead)
	# rw_lead=rwk.Lead(sport)
	# rw_inLead=rwk.inLead(rw_lead)
	# rw=rwk.lastChange(rw_inLead)
	sm_lead=sm.Lead(sport)
	#sm_inLead=sm.inLead(sm_lead)
	#sr=sm.lastChange(sm_inLead)
	msr,sr=lt.maxLeadTime(sm_lead)

	h,b=np.histogram(s, bins)
	hcorr=h/(binw*len(s))
	plt.scatter(b[:len(bins)-1], hcorr, c='blue',marker='o',label=sport+' games, seasons '+seasons) 
	hr,br=np.histogram(sr,bins)
	hrcorr=hr/(binw*len(sr))
	plt.plot(br[:len(bins)-1],hrcorr,c='green',linewidth=2,label='Inhomogeneous Poisson Process')
	#ubiased RW
	# rwstep=20.0
	# rwbins=scope/rwstep
	# h,b=np.histogram(rw, rwbins)
	# hcorr=h/(rwstep*len(rw))
	# plt.plot(b[:rwbins], hcorr, c='orange',linewidth=2.5,label='Homogenous Poisson Process') 
	x=np.array(range(scope)) #arcsine law
	y=1/(np.pi*(x*(scope+1-x))**(0.5))
	plt.plot(x,y,'r',linewidth=2,label='Arcsine Law')
	plt.xlim(xmin=0,xmax=scope)
	plt.ylim(ymin=0,ymax=0.0027)
	plt.legend()
	plt.xlabel('Clock time (seconds)')
	plt.ylabel('Probability of maximum lead')
	#plt.savefig(sport+'varBinnedUpdate.pdf')
	#plt.close()
	plt.show()
