import leadOverTimeLatest as lt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

sport='NBA'
data=lt.getData(sport)
lead=lt.Lead(data,sport)
inLead=lt.inLead(lead)
tr=lt.lastChangeMessy(inLead)
safe=lt.assignSafety(tr,sport)
tuples=lt.getZ(lead,safe,sport)
df=pd.DataFrame(tuples)

step=0.02
bins=np.arange(min(df[0]),max(df[0]),step)
df[2]=np.digitize(df[0],bins) #assign a bin number to each tuple
gr=df[1].groupby(df[2]) #not all the bin numbers are present!
ave_q=gr.mean()
bin_nums=np.sort(df[2].unique())
z=[bins[i-1] for i in bin_nums]
plt.scatter(z,ave_q)
plt.show()