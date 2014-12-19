import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import svm, datasets, cross_validation

data=pandas.DataFrame.from_csv('timeLeadSafeTrainAll_sample.csv',header=None, index_col=None)
data=data.as_matrix()
X=data[:,2:4]
y=data[:,4]

cv=cross_validation.StratifiedKFold(y, n_folds=10)
C=[0.01,0.1,0.3,1,3,10,100,1000]
acc=np.zeros(len(C))
spread=np.zeros(len(C))
index=0
for c in C:
	clf=svm.LinearSVC(C=c)
	scores=cross_validation.cross_val_score(clf,X,y,cv=cv)
	acc[index]=scores.mean()
	spread[index]=scores.std()
	index+=1
acc.tofile('linSVMacc.txt',sep=',')
spread.tofile('linSVMspread.txt',sep=',')