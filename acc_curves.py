import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import linear_model, svm

data=pandas.DataFrame.from_csv('timeLeadSafeTrainAll_sample.csv',header=None, index_col=None)
dm=data.as_matrix()
X=dm[:,2:4]
y=dm[:,4]
test=pandas.DataFrame.from_csv('timeLeadSafeTestAll_sample.csv',header=None, index_col=None)
tm=test.as_matrix()
X_test=tm[:,2:4]
y_test=tm[:,4]

logReg=linear_model.LogisticRegression(penalty='l1').fit(X,y)
#lin_svc=svm.LinearSVC(C=1).fit(X,y)

test[5]=logReg.predict(X_test) #prediction
test[6]=test[4]==test[5] #overall accuracy
test[7]=(test[4]==test[5])&(test[4]==1) #true positives
test[8]=(test[4]==test[5])&(test[4]==0) #true negatives
gr=test.groupby(0)
accVec=gr[6].apply(lambda x: sum(x)/float(len(x)))
tpVec=gr[7].apply(lambda x: sum(x)/float(len(x)))
tnVec=gr[8].apply(lambda x: sum(x)/float(len(x)))

plt.plot(accVec.index.values,accVec,'b')
plt.plot(tpVec.index.values,tpVec,'g-')
plt.plot(tnVec.index.values,tnVec,'r--')
plt.xlim(xmin=0,xmax=scope+2)
plt.xlabel('Elapsed time, t (seconds)')
plt.ylabel('Rate')
plt.title('Logistic regression accuracy curves')
plt.legend(('accuracy','true positive','true negative'),loc=6)
plt.show()
