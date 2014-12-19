import numpy as np
import matplotlib.pyplot as plt

def plot(t,slead):
	m=max(slead)
	H,xedges,yedges=np.histogram2d(t,slead,bins=(959,m))
	#t and slead are just lists - not matrices!
	extent=[xedges[0],xedges[-1],yedges[0],yedges[-1]]

	# H needs to be rotated and flipped
	H = np.rot90(H)
	H = np.flipud(H)
	 
	# Mask zeros
	Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value of zero
	 
	# Plot 2D histogram using pcolor
	fig = plt.figure()
	plt.pcolormesh(xedges,yedges,Hmasked/float(len(slead)))
	plt.xlabel('time elapsed')
	plt.ylabel('lead')
	cbar = plt.colorbar()
	cbar.ax.set_ylabel('Frequency')
	plt.xlim(xmin=0,xmax=2880)
	plt.ylim(ymin=0)
	plt.show()