from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
import pandas as pd

# Hyperparameters
S = 10
lmbda = 1e-5
neuronsPerLayer = 100
layers = 3

# Read Data
fname = 'airfoil.xls'
airfoil_data = pd.read_excel(fname, 0)  # load data as pandas data frame
T = airfoil_data.values[:, 5]           # target values = noise load (= column 5 of data table)
X = airfoil_data.values[:, :5]          # feature vectors (= column 0-4 of data table)

# Scale Data for good Numeric stability
scaler = StandardScaler()
scaler.fit(X)
X = scaler.transform(X)

# Create MLP and Cross Validate it
crossValid = KFold(n_splits=S, shuffle=True, random_state=1)
mlp = MLPRegressor(solver="lbfgs", alpha=lmbda, hidden_layer_sizes=(neuronsPerLayer, layers), random_state=1, max_iter=500)

for i, (train_index, test_index) in enumerate(crossValid.split(X, T)):
    X_train, X_test = X[train_index], X[test_index]
    T_train, T_test = T[train_index], T[test_index]

    mlp.fit(X_train, T_train)

    # Use Mean Squared Error (MSE) for regression evaluation
    train_predictions = mlp.predict(X_train)
    test_predictions = mlp.predict(X_test)

    train_mse = mean_squared_error(T_train, train_predictions)
    test_mse = mean_squared_error(T_test, test_predictions)

    print(f'Fold {i+1}: Training MSE - {train_mse}, Test MSE - {test_mse}')
