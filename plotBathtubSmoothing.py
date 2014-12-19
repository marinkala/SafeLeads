def movingaverage(interval, window_size):
    window= numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')

start=min(s)
scope=3600
step=20.0
window=10
bins=(scope-start)/step
h,b=np.histogram(s, bins, normed=True)
#plt.scatter(b[:bins],h,c='blue',marker='o') #actual data
h_av=movingaverage(h,window)
plt.scatter(b[:bins], h_av, c='blue',marker='o',label='Empirical data') 
#smoothed empirical data
binsRW=scope/step
hrw,brw=np.histogram(sr, binsRW, normed=True)
hrw_av=movingaverage(hrw,window)
plt.plot(brw[:binsRW], hrw_av, 'r',linewidth=2,label='Unbiased Random Walk')
plt.xlim(xmin=0,xmax=scope)
plt.ylim(ymin=0,ymax=0.001)
plt.legend()
plt.xlabel('Clock time (seconds)')
plt.ylabel('Probability of last lead change')
