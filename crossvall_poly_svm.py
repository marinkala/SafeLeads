import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import svm, datasets, cross_validation

k=5
#this should be a function - read in data and divide into train/test
data=pandas.DataFrame.from_csv('timeLeadSafeAll_sample.csv',header=None, index_col=None)
data=data.as_matrix()
X=data[:,2:4]
y=data[:,4]
X_train, X_test, y_train, y_test = cross_validation.train_test_split(\
    X, y, test_size=0.3, random_state=0)

C=[0.01,0.1,1.0,10.0,100.0,1000.0]
deg=[0.3,0.5,2.0,3.0]
acc=pandas.DataFrame(index=deg,columns=C)
spread=pandas.DataFrame(index=deg,columns=C)
maxn=0
maxpar=[0,0]
for d in deg:
	for c in C:
		clf=svm.SVC(kernel='poly',degree=d, C=c)
		scores=cross_validation.cross_val_score(clf,X_train,y_train,cv=k)
		acc.loc[d,c]=scores.mean()
		spread.loc[d,c]=scores.std()
		if scores.mean()>maxn:
			maxn=scores.mean()
			maxpar=[d,c]
acc.to_csv('PolySVMacc.csv')
spread.to_csv('PolySVMspread.csv')
df=pandas.DataFrame(maxpar,index=['deg','c'])
df.to_csv('PolySVMpars.csv',header=False)