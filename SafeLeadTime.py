import numpy  as np

t=np.zeros(len(inLeadA))
for i in xrange(len(inLeadA)):
    a=inLeadA[i][1:].tostring().find('\x01')/4+1
    b=inLeadB[i][1:].tostring().find('\x01')/4+1
    t[i]=max(a,b)
#OR
t=np.zeros(len(inLeadA))
for i in xrange(len(inLeadA)):
	try:
		t[i]=np.where(inLeadA[i][1:]==1)[0][0]+1
	except IndexError:
		try:
			t[i]=np.where(inLeadB[i][1:]==1)[0][0]+1
		except IndexError:
			t[i]=-1
s=t[t>-1]


start=inLeadB[0][1:].tostring().find('\x01')/4+1
#OR
start=np.where(inLeadA[0][1:]==1)[0][0]+1
plt.plot(range(1,2881),LeadB[41][1:])
plt.axvline(x=start,color='r')
plt.axhline(y=0, xmax=2880,linestyle='--',color='g')
plt.show()

cross=np.where(np.diff(np.sign(LeadA[0][:])))