data=lt.getData('NHL')
lead=lt.Lead(data,'NHL')
inLead=lt.inLead(lead)
fc=lt.firstChange(inLead)

scope=3600
step=30.0

prop=len(fc[fc==-1])/float(len(fc))
first=fc[fc>0]
h, b=np.histogram(first, scope/step)
hcorr=h/(len(first)*step)
plt.scatter(b[:len(b)-1],hcorr,c='blue',marker='o')
plt.xlim(xmin=0,xmax=scope)
plt.ylim(ymin=0, ymax=0.008)
plt.xlabel('Time of the first lead change')
plt.ylabel('Relative Frequency')
plt.show()

NHL: prop=0.3610
NFL: prop=0.3482
CFB: prop=0.4284
NBA: prop=0.0633

