slead=[]
stime=[]
ulead=[]
utime=[]
for i in xrange(games):
	fin_sign=np.sign(lead[i,scope-1])
	for j in xrange(scope):
		if lead[i,j]!=0: #only keep nonzero leads and corresponding times
			#for the winning team
			if j<t[i]: #if before the safe lead time
				if fin_sign*lead[i,j]>0:
					ulead.append(fin_sign*lead[i,j])
					utime.append(j+1)#to start time with second 1
			else: #if during or after safe lead time
				slead.append(fin_sign*lead[i,j])
				stime.append(j+1)
			#for the losing team
			if -lead[i,j]*fin_sign>0:
				ulead.append(-lead[i,j]*fin_sign)
				utime.append(j+1)