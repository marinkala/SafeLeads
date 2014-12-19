start=min(s)
scope=3600
step=20
bins=(scope-start)/float(step)
h,b=np.histogram(s, bins, normed=True)
plt.scatter(b[:bins],h,c='blue',marker='o')
plt.xlim(xmin=0,xmax=scope)
plt.ylim(ymin=0)
plt.xlabel('Clock time (seconds)')
plt.ylabel('Probability of last lead change')
