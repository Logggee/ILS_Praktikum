from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
import pandas as pd
import numpy as np

# Hyperparameter
S = 3
lmbda = 1e-5
nNeighbours = 5


# (II) Load data 
fname='airfoil.xls'
airfoil_data = pd.read_excel(fname,0); # load data as pandas data frame 
T = airfoil_data.values[:,5]           # target values = noise load (= column 5 of data table)
X = airfoil_data.values[:,:5]          # feature vectors (= column 0-4 of data table)

# scale Data for good Numaric stability
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# create MLP and Cross Validate it
crossValid = KFold(n_splits=S)

for i, (train_index, test_index) in enumerate(crossValid.split(X,T)):
    X_train, X_test = X[train_index], X[test_index]         # numpay arrays can be indexed with a list
    T_train, T_test = T[train_index], T[test_index]

    knn = KNeighborsRegressor(n_neighbors=nNeighbours)
    knn.fit(X_train, T_train)                               # train model with train data

    print(f'Fold {i+1}: Training Accuracy - {knn.score(X_train, T_train)}, Test Accuracy - {knn.score(X_test, T_test)}')    # evaluate model

    # Calculate MEA and MAPE for training and test data
    predictions_train = knn.predict(X_train)
    predictions_test = knn.predict(X_test)

    mae_train = mean_absolute_error(T_train, predictions_train)
    mae_test = mean_absolute_error(T_test, predictions_test)

    mape_train = mean_absolute_percentage_error(T_train, predictions_train)
    mape_test = mean_absolute_percentage_error(T_test, predictions_test)

    print(f'Fold {i+1}: Training R^2 - {knn.score(X_train, T_train)}, Test R^2 - {knn.score(X_test, T_test)}')
    print(f'     Training MAE - {mae_train}, Test MAE - {mae_test}')
    print(f'     Training MAPE - {mape_train}, Test MAPE - {mape_test}')