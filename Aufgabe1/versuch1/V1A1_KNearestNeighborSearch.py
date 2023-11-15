# Programmgeruest zu Versuch 1, Aufgabe 1
import numpy as np

def getKNearestNeighbors(x,X,k=1):  # realizes nearest neighbor search of x in database
    """
    compute the k nearest neighbors for a query vector x given a data matrix X
    :param x: the query vector x
    :param X: the N x D data matrix (in each row there is data vector) as a numpy array
    :param k: number of nearest-neighbors to be returned
    :return: return list of k line indixes referring to the k nearest neighbors of x in X
    """
    return np.argsort([np.linalg.norm(x - i) for i in X])[:k]           # REPLACE! return indexes of k smallest distances 

def getClassProbabilities(t):
    values, counts = np.unique(t, return_counts=True)
    amountOfEachClass = dict(zip(values, counts))
    return  dict(zip(values, [(amountOfEachClass[x] / len(t)) * 100  for x in amountOfEachClass])) #Prozentuale vorkommniswarscheinlichkeit der Klassen

def classify(P):
    return max(P, key=lambda k: (P[k], -list(P.keys()).index(k))) #sortiert das dict nach den values und holt sich dann den letzten key 

# ***** MAIN PROGRAM ********

# (i) Generate dummy data 
X = np.array([[1,2,3],[-2,3,4],[3,-4,5],[4,5,-6],[-5,6,7],[6,-7,8]]);      # data matrix X: list of data vectors (=database) of dimension D=3
T = np.array([1,1,1,1,2,2])
x = np.array([3.5,-4.4,5.3]);                          # a test data vector
print("Data matrix X=\n",X)
print("Test vector x=",x)

# (ii) Print all Euklidean distances to test vector x
print("Euklidean distances to x: ", [np.linalg.norm(x - i) for i in X])  # REPLACE! compute list of Euklidean distances   

# (iii) Search for k nearest neighbor
k=3
idx_knn = getKNearestNeighbors(x,X,k)                  # get indexes of k nearest neighbors
print("idx_knn=",idx_knn)

# (iv) output results
print("The k Nearest Neighbors of x are the following vectors:")
for i in range(k):
    idx=idx_knn[i]
    print("The", i+1, "th nearest neighbor is: X[",idx,"]=",X[idx]," with distance ", np.linalg.norm(X[idx]-x))

P = getClassProbabilities(T)
print("Die Klassen kommen zu ", P, "% vor.")

C = classify(P)
print("Die Klasse mit der Höchsten Warscheinlichkeit und dem kleinsten Index ist: ", C)