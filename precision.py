#!/usr/bin/python

from __future__ import division
import sys

def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average prescision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
    A list of elements that are to be predicted (order doesn't matter)
    predicted : list
    A list of predicted elements (order does matter)
    k : int, optional
    The maximum number of predicted elements

    Returns
    -------
    score : double
    The average precision at k over the input lists

    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 1.0

    return score / min(len(actual), k)

if __name__ == "__main__":
    data = []

    with open(sys.argv[1]) as dataset, open(sys.argv[2]) as results:
        results.readline() # get rid of header
        counter = 0
        for data_line, results_line in zip(dataset, results):
            prob = results_line.rstrip().split(" ")
            data.append([counter, int(data_line.split(" ")[0]), float(prob[2])])
            counter += 1

    data_s = sorted(data, key=lambda x: -x[2]) # sort by probability to be true

    relevant = set([x[0] for x in data_s if x[1] == 1])
    ranking = [x[0] for x in data_s]

    print "k=10  ", apk(relevant, ranking, k=10)
    print "k=50  ", apk(relevant, ranking, k=50)
    print "k=100 ", apk(relevant, ranking, k=100)
    print "k=500 ", apk(relevant, ranking, k=500)
    print "k=1000", apk(relevant, ranking, k=1000)
    print "k=1500", apk(relevant, ranking, k=1500)
    print "k=2000", apk(relevant, ranking, k=2000)
    print "k=2500", apk(relevant, ranking, k=2500)

