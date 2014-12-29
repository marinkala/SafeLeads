l1teams=gameLead['0'][(abs(gameLead['1'])<=5) & (gameLead['1']>0)]
datat1=data[data.GAME_CODE.isin(l1teams)]
q1=lt.getBias(datat1)
lead1=lt.Lead(datat1, 'NBA')
inl1=lt.inLead(lead1)
s1=lt.lastChange(inl1)
binw=getBinWidth(bins)
p=91.99/scope
v1=((2*q1-1)/p)**2
D=1/(4*p)
h,b=np.histogram(s1, bins)
hcorr=h/(binw*len(s1))
plt.scatter(b[:len(bins)-1], hcorr, c='blue',marker='o',label='Empirical data')
x=np.array(range(scope))
y=(np.exp((-v1**2*x)/(4*D))/(np.pi*(x*(scope+1-x))**0.5))*((((np.pi*v1**2*(scope+1-x))/(4*D))**0.5)*\
scipy.special.erf(((v1**2*(scope+1-x))/(4*D))**0.5)+np.exp((v1**2*(scope+1-x))/(4*D)))