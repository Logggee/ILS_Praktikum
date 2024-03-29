from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold
import pandas as pd
import numpy as np

# Hyperparameter
S = 5
lmbda = 1
neuronsPerLayer = 10
layers = 2

#Read Data und transform in to numpy
forestdata  = pd.read_csv('training.csv'); # load data as pandas data frame 
classlabels = ['s','h','d','o'];                                      # possible class labels (C=4) 
classidx    = {classlabels[i]:i for i in range(len(classlabels))}     # dict for mapping classlabel to index 
T_txt = forestdata.values[:,0]           # array of class labels of data vectors (class label is first data attribute)
X = forestdata.values[:,1:]           # array of feature vectors (features are remaining attributes)
T = [classidx[t.strip()] for t in T_txt]          # transform text labels 's','h','d','o' to numeric lables 0,1,2,3
X,T=np.array(X,'float'),np.array(T,'int')  # convert to numpy arrays

# scale Data for good Numaric stability
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# create MLP and Cross Validate it
crossValid = StratifiedKFold(n_splits=S)

for i, (train_index, test_index) in enumerate(crossValid.split(X,T)):
    X_train, X_test = X[train_index], X[test_index]         # numpay arrays können mit listen indiziert werden
    T_train, T_test = T[train_index], T[test_index]

    mlp = MLPClassifier(solver="lbfgs", alpha=lmbda, hidden_layer_sizes=(neuronsPerLayer, layers), random_state=1, activation='tanh', max_iter=500)
    mlp.fit(X_train, T_train)

    print(f'Fold {i+1}: Training Accuracy - {mlp.score(X_train, T_train)}, Test Accuracy - {mlp.score(X_test, T_test)}')