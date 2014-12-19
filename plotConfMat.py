from sklearn.metrics import confusion_matrix

pred=logReg.predict(X_test)
cm=confusion_matrix(y_test,pred)
cmn=cm/float(sum(sum(cm)))
plt.matshow(cmn)
plt.title('Confusion matrix')
plt.colorbar()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.show()