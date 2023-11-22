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

# *****************************************************************************
# ***** MAIN PROGRAM: Test nearest neighbor search and classification  ********
# *****************************************************************************
if __name__ == '__main__':
    
    # (i) Generate some dummy data 
    X = np.array([[1,2,3],[-2,3,4],[3,-4,5],[4,5,-6],[-5,6,7],[6,-7,8]])   # data matrix X: list of data vectors (=database) of dimension D=3
    t = np.array( [0     ,1       ,2       ,0       ,1       ,2      ] )   # class labels (C=3 classes)
    C = np.max(t)+1                                                        # C=3 here
    x = np.array([3.5,-4.4,5.3]);                                          # a new input vector to be classified
    print("Data matrix X=\n",X)
    print("Class labels t=",t)
    print("Test vector x=",x)
    
    # (ii) Print all Euklidean distances to test vector x
    print("Euklidean distances to x: ", [np.linalg.norm(X[i]-x) for i in range(len(X))])
    
    # (iii) Search for K nearest neighbor
    K=3                                                    # define K
    idx_KNN = getKNearestNeighbors(x,X,K)                  # get indexes of k nearest neighbors
    print("idx_KNN=",idx_KNN)
    print("The K Nearest Neighbors of x are the following vectors:")
    for i in range(K):
        idx=idx_KNN[i]
        print("The", i+1, "th nearest neighbor is: X[",idx,"]=",X[idx]," with distance ", np.linalg.norm(X[idx]-x)," and class label ",t[idx])

    # (iv) do classification
    P=getClassProbabilities(t)                # get class probabilities for input x
    c=classify(P)                             # get most likely class
        
    print("Class distribution P=",P)
    print("Most likely class: c=",c," with P(c)=",P[c])
