import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import linear_model, cross_validation

data=pandas.DataFrame.from_csv('timeLeadSafeTrainAll_sample.csv',header=None, index_col=None)
data=data.as_matrix()
X=data[:,2:4]
y=data[:,4]

cv=cross_validation.StratifiedKFold(y, n_folds=10)
pen=['l1','l2']
acc=np.zeros(len(pen))
spread=np.zeros(len(pen))
row_ind=0
for p in pen:
	clf=linear_model.LogisticRegression(penalty=p)
	scores=cross_validation.cross_val_score(clf,X,y,cv=cv)
	acc[row_ind]=scores.mean()
	spread[row_ind]=scores.std()
	row_ind+=1
acc.tofile('LogRegacc.txt',sep=',')
spread.tofile('LogRegspread.txt',sep=',')