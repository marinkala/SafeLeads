import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import svm, datasets

data=pandas.DataFrame.from_csv('NBA_res/timeLeadSafe_sample.csv',header=None, index_col=None)
data=data.as_matrix()
X=data[:,2:4]
y=data[:,4]
test=pandas.DataFrame.from_csv('NBA_res/timeLeadSafe_test_sample.csv',header=None, index_col=None)
test=test.as_matrix()
X_test=test[:,2:4]
y_test=test[:,4]
lin_svc=svm.LinearSVC(C=1).fit(X,y)
h=0.02
x_min, x_max = X[:,0].min() - 0.2, X[:,0].max() + 0.2
y_min, y_max = X[:,1].min() - 0.2, X[:,1].max() + 0.2
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h))
Z=lin_svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
#plt.countour(xx,yy,Z) - for just a line!!!
#plt.axis('off')
plt.scatter(X[:,0], X[:,1], c=y, cmap=plt.cm.Paired)
plt.title('SVM with linear kernel on 1% of the data')
plt.show()

pred=lin_svc.predict(X_test)
acc=sum(pred==y_test)/float(len(pred)) 
tp=sum((pred==y_test)&(y_test==1))/float(len(pred)) 
tn=sum((pred==y_test)&(y_test==0))/float(len(pred))
fn=sum((pred!=y_test)&(y_test==1))/float(len(pred))
fp=sum((pred!=y_test)&(y_test==0))/float(len(pred))