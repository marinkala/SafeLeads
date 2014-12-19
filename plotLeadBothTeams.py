game=0
s=np.sign(LeadA[game])
s[0]=0 #the game code
s[s==0]=-1 #replace 0 so they don't count as crossings
cross=np.where(np.diff(s))[0]
colors=['r','b']

a=True
if LeadA[game][cross[0]+1]<0:
	a=not a

fig, ax=plt.subplots()
c=colors[int(a)]
ax.plot(range(1,cross[0]+1),LeadB[game][1:cross[0]+1])
ax.vlines(x=cross[0]+1,ymin=LeadB[game][cross[0]],ymax=0)
for i in xrange(len(cross)):
	start=cross[i]+1
	if i==len(cross)-1:
		fin=2880
	else:
		fin=cross[i+1]+1
	c=colors[int(a)]
	if a:
		ax.vlines(x=start,ymin=0,ymax=LeadA[game][start],color=c)
		ax.plot(range(start,fin),LeadA[game][start:fin],color=c)
		if i!=(len(cross)-1):
			ax.vlines(x=fin,ymin=0,ymax=LeadA[game][fin-1],color=c)
	else:
		ax.vlines(x=start,ymin=LeadB[game][start],ymax=0,color=c)
		ax.plot(range(start,fin),LeadB[game][start:fin],color=c)
		if i!=(len(cross)-1):
			ax.vlines(x=fin,ymin=LeadB[game][fin-1],ymax=0,color=c)
	a=not a
ax.axvline(x=cross[i]+1, color='g')