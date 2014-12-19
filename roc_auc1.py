import numpy as np
import pandas
import matplotlib.pyplot as plt
from sklearn import linear_model, svm
from sklearn.metrics import roc_curve, auc
import predict_distNaive as pdn

data=pandas.DataFrame.from_csv('timeLeadSafeTrainAll_sample.csv',header=None, index_col=None)
dm=data.as_matrix()
X=dm[:,2:4]
y=dm[:,4]
test=pandas.DataFrame.from_csv('timeLeadSafeTestAll_sample.csv',header=None, index_col=None)
tm=test.as_matrix()
X_test=tm[:,2:4]
y_test=tm[:,4]
scope=2880
start=int(min(tm[:,0]))

#logReg=linear_model.LogisticRegression(penalty='l1').fit(X,y)
#clf=svm.SVC(C=0.1,kernel='linear',probability=True).fit(X,y)
roc_auc=np.zeros(len(range(start,scope+1)))
for i in xrange(len(range(start,scope+1))):
	test_i=tm[tm[:,0]<=i+start]
	y_i=y_test[tm[:,0]<=i+start]
	#prob=clf.predict_proba(test_i) #where time is le than i
	prob=pdn.predict_dist(test_i)
	fpr,tpr,thresh=roc_curve(y_i,prob)
	try:
		roc_auc[i]=auc(fpr,tpr)
	except ValueError:
		tpr_c=np.nan_to_num(tpr)
		roc_auc[i]=auc(fpr,tpr_c)
plt.clf()
plt.plot(range(start,scope+1),roc_auc,linewidth=2,c='g')
plt.xlim(xmax=scope+1)
plt.xlabel('Time t, second')
plt.ylabel('ROC AUC')
plt.title('Bill James on test data with time less or equal to t')
plt.show()

#plt.clf()
#plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
#plt.plot([0, 1], [0, 1], 'k--')
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.0])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('Receiver operating characteristic curve')
#plt.legend(loc="lower right")
#plt.show()