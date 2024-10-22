#
#  tsne.py
#
# Implementation of t-SNE in Python. The implementation was tested on Python 2.5.1, and it requires a working
# installation of NumPy. The implementation comes with an example on the MNIST dataset. In order to plot the
# results of this example, a working installation of matplotlib is required.
# The example can be run by executing: ipython tsne.py -pylab
#
#
#  Created by Laurens van der Maaten on 20-12-08.
#  Copyright (c) 2008 Tilburg University. All rights reserved.

# Modified by Federico Giraud, Eurecom, Sophia Antipolis, France

import sys
import numpy as Math
import pylab as Plot
from mpl_toolkits.mplot3d import Axes3D

def Hbeta(D = Math.array([]), beta = 1.0):
    """Compute the perplexity and the P-row for a specific value of the precision of a Gaussian distribution."""

    # Compute P-row and corresponding perplexity
    P = Math.exp(-D.copy() * beta);
    sumP = sum(P);
    if sumP == 0:
        sumP = 0.1
    H = Math.log(sumP) + beta * Math.sum(D * P) / sumP;
    P = P / sumP;
    return H, P;


def x2p(X = Math.array([]), tol = 1e-5, perplexity = 30.0):
    """Performs a binary search to get P-values in such a way that each conditional Gaussian has the same perplexity."""

    # Initialize some variables
    print "Computing pairwise distances..."
    (n, d) = X.shape;
    sum_X = Math.sum(Math.square(X), 1);
    D = Math.add(Math.add(-2 * Math.dot(X, X.T), sum_X).T, sum_X);
    P = Math.zeros((n, n));
    beta = Math.ones((n, 1));
    logU = Math.log(perplexity);

    # Loop over all datapoints
    for i in range(n):
        # Print progress
        if i % 500 == 0:
            print "Computing P-values for point ", i, " of ", n, "..."

        # Compute the Gaussian kernel and entropy for the current precision
        betamin = -Math.inf;
        betamax =  Math.inf;
        Di = D[i, Math.concatenate((Math.r_[0:i], Math.r_[i+1:n]))];
        (H, thisP) = Hbeta(Di, beta[i]);
        # BOH

        # Evaluate whether the perplexity is within tolerance
        Hdiff = H - logU;
        tries = 0;
        while Math.abs(Hdiff) > tol and tries < 50:

            # If not, increase or decrease precision
            if Hdiff > 0:
                betamin = beta[i];
                if betamax == Math.inf or betamax == -Math.inf:
                    beta[i] = beta[i] * 2;
                else:
                    beta[i] = (beta[i] + betamax) / 2;
            else:
                betamax = beta[i];
                if betamin == Math.inf or betamin == -Math.inf:
                    beta[i] = beta[i] / 2;
                else:
                    beta[i] = (beta[i] + betamin) / 2;

            # Recompute the values
            (H, thisP) = Hbeta(Di, beta[i]);
            Hdiff = H - logU;
            tries = tries + 1;

        #print thisP
        # Set the final row of P
        P[i, Math.concatenate((Math.r_[0:i], Math.r_[i+1:n]))] = thisP;

    # Return final P-matrix
    print "Mean value of sigma: ", Math.mean(Math.sqrt(1 / beta))
    return P;


def pca(X = Math.array([]), no_dims = 50):
    """Runs PCA on the NxD array X in order to reduce its dimensionality to no_dims dimensions."""

    print "Preprocessing the data using PCA..."
    (n, d) = X.shape;
    print "1"
    X = X - Math.tile(Math.mean(X, 0), (n, 1));
    print "2"
    (l, M) = Math.linalg.eig(Math.dot(X.T, X));
    print "3"
    Y = Math.dot(X, M[:,0:no_dims]);
    print "DONE"
    return Y;


def tsne(X = Math.array([]), no_dims = 2, PCA_dims = None, perplexity = 30.0, max_iter=300):
    """Runs t-SNE on the dataset in the NxD array X to reduce its dimensionality to no_dims dimensions.
    The syntaxis of the function is Y = tsne.tsne(X, no_dims, perplexity), where X is an NxD NumPy array."""

    # Check inputs
    if X.dtype != "float64":
        print "Error: array X should have type float64.";
        return -1;
    #if no_dims.__class__ != "<type 'int'>":            # doesn't work yet!
    #    print "Error: number of dimensions should be an integer.";
    #    return -1;

    # Initialize variables
    if PCA_dims:
        X = pca(X, PCA_dims);
    (n, d) = X.shape;
    #max_iter = 100;
    initial_momentum = 0.5;
    final_momentum = 0.8;
    eta = 500;
    min_gain = 0.01;
    Y = Math.random.randn(n, no_dims);
    dY = Math.zeros((n, no_dims));
    iY = Math.zeros((n, no_dims));
    gains = Math.ones((n, no_dims));

    # Compute P-values
    P = x2p(X, 1e-5, perplexity);
    P = P + Math.transpose(P);
    P = P / Math.sum(P);
    P = P * 4;                                    # early exaggeration
    P = Math.maximum(P, 1e-12);

    # Run iterations
    for iter in range(max_iter):

        # Compute pairwise affinities
        sum_Y = Math.sum(Math.square(Y), 1);
        num = 1 / (1 + Math.add(Math.add(-2 * Math.dot(Y, Y.T), sum_Y).T, sum_Y));
        num[range(n), range(n)] = 0;
        Q = num / Math.sum(num);
        Q = Math.maximum(Q, 1e-12);

        # Compute gradient
        PQ = P - Q;
        for i in range(n):
            dY[i,:] = Math.sum(Math.tile(PQ[:,i] * num[:,i], (no_dims, 1)).T * (Y[i,:] - Y), 0);

        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum
        gains = (gains + 0.2) * ((dY > 0) != (iY > 0)) + (gains * 0.8) * ((dY > 0) == (iY > 0));
        gains[gains < min_gain] = min_gain;
        iY = momentum * iY - eta * (gains * dY);
        Y = Y + iY;
        Y = Y - Math.tile(Math.mean(Y, 0), (n, 1));

        # Compute current value of cost function
        if (iter + 1) % 10 == 0:
            C = Math.sum(P * Math.log(P / Q));
            print "Iteration ", (iter + 1), ": error is ", C

        # Stop lying about P-values
        if iter == 100:
            P = P / 4;

    # Return solution
    return Y;


if __name__ == "NOOO__main__":
    #print "Run Y = tsne.tsne(X, no_dims, perplexity) to perform t-SNE on your dataset."
    #print "Running example on 2,500 MNIST digits..."
    #X = Math.loadtxt("mnist2500_X.txt");
    #labels = Math.loadtxt("mnist2500_labels.txt");
    print "Loading file"
    X1 = Math.loadtxt("../features_test")
    #X1 = Math.loadtxt("300_14/imagenet_features");
    #labels = Math.loadtxt("400_14/imagenet_labels");
    #X = Math.array([[n/100 for n in x] for x in X1[0:1705]])
    print "Resizing values"
    X = X1/100
    #Y = tsne(X, 2, 50, 20.0);
    print "Running tsne"
    Y = tsne(X[:100], 2, perplexity=20.0, max_iter=400)
    #labels = Math.array([Math.float64(1)]*386 + [Math.float64(2)]*1079 + [Math.float64(3)]*240 + [Math.float64(4)]*1226)
    #fig = Plot.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(Y[:,0][0:99], Y[:,1][0:99], Y[:,2][0:99], color='b', label="dog");
    #ax.scatter(Y[:,0][99:189], Y[:,1][99:189], Y[:,2][99:189], color='r', label="cat");
    #ax.scatter(Y[:,0][189:297], Y[:,1][189:297], Y[:,2][189:297], color='g', label="bird");
    labels = Math.array([Math.float64(1)]*386 + [Math.float64(2)]*1079 + [Math.float64(3)]*240 + [Math.float64(4)]*1226)
    Plot.scatter(Y[:,0][0:386], Y[:,1][0:386], 20, color='b', label="dog", alpha=0.5);
    Plot.scatter(Y[:,0][386:1465], Y[:,1][386:1465], 20, color='r', label="cat", alpha=0.5);
    Plot.scatter(Y[:,0][1465:1705], Y[:,1][1465:1705], 20, color='g', label="bird", alpha=0.5);
    Plot.scatter(Y[:,0][1705:2931], Y[:,1][1705:2931], 20, color='y', label="lamp", alpha=0.5);
    Plot.legend(loc=0, scatterpoints = 1)
    Plot.show()

if __name__ == "__main__":
    print "Loading file"
    positives = []
    negatives = []
    with open(sys.argv[1]) as input:
        for line in input:
            eol = line.find("#")
            if eol > 0:
                line = line[:eol]
            words = line.rstrip().split(" ")
            values = [0] * int(sys.argv[2])
            for w in words[1:]:
                d = w.split(":")
                values[int(d[0])-1] = float(d[1])
            if words[0] == "0":
                negatives.append(values)
            else:
                positives.append(values)
    positives = positives[:400]
    negatives = negatives[:400]
    n_pos = len(positives)
    n_neg = len(negatives)
    X = Math.array(positives + negatives, dtype=Math.float64)
    print "Resizing values"
    print "Running tsne"
    Y = tsne(X, 2, perplexity=20.0, max_iter=400)
    #labels = Math.array([Math.float64(1)]*386 + [Math.float64(2)]*1079 + [Math.float64(3)]*240 + [Math.float64(4)]*1226)
    #fig = Plot.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(Y[:,0][0:99], Y[:,1][0:99], Y[:,2][0:99], color='b', label="dog");
    #ax.scatter(Y[:,0][99:189], Y[:,1][99:189], Y[:,2][99:189], color='r', label="cat");
    #ax.scatter(Y[:,0][189:297], Y[:,1][189:297], Y[:,2][189:297], color='g', label="bird");
    labels = Math.array([Math.float64(1)]*n_pos + [Math.float64(2)]*n_neg)
    Plot.scatter(Y[:,0][0:n_pos], Y[:,1][0:n_pos], 20, color='r', label="Positive", alpha=0.5);
    Plot.scatter(Y[:,0][n_pos:n_pos+n_neg], Y[:,1][n_pos:n_pos+n_neg], 20, color='b', label="Negative", alpha=0.5);
    Plot.legend(loc=0, scatterpoints = 1)
    Plot.show()
