#Bill James
scope=2880
pred=test[1]>(scope-test[0])**0.5+3

#Naive
pred=np.ones(len(y_test))
