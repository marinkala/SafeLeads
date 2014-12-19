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
gamma=[0.0001,0.01,1.0,100.0]
acc=pandas.DataFrame(index=gamma,columns=C)
spread=pandas.DataFrame(index=gamma,columns=C)
maxn=0
maxpar=[0,0]
for g in gamma:
	for c in C:
		clf=svm.SVC(kernel='rbf',gamma=g, C=c)
		scores=cross_validation.cross_val_score(clf,X_train,y_train,cv=k)
		acc.loc[g,c]=scores.mean()
		spread.loc[g,c]=scores.std()
		if scores.mean()>maxn:
			maxn=scores.mean()
			maxpar=[g,c]
acc.to_csv('GaussSVMacc.csv')
spread.to_csv('GaussSVMspread.csv')
df=pandas.DataFrame(maxpar,index=['gamma','c'])
df.to_csv('GaussSVMpars.csv',header=False)