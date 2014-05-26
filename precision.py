#!/usr/python

from __future__ import division
import sys

data = []

with open(sys.argv[1]) as dataset, open(sys.argv[2]) as results:
    results.readline() # get rid of header
    counter = 0
    for data_line, results_line in zip(dataset, results):
        prob = results_line.rstrip().split(" ")
        data.append([counter, int(data_line.split(" ")[0]), float(prob[1]), float(prob[2])])
        counter += 1

def gen_ranking(data, k):
    data_s = sorted(data, key=lambda x: -x[3]) # sort by probability to be true

    relevant = set()
    ranking = []

    for n, real, p0, p1 in data_s[:k]:
        if real == 1:
            relevant.add(n)    # is a relevant document
        if p1 >= 0.5:
            ranking.append(n)  # is in ranking

    return ranking, relevant

def calc_classification(data, threshold=0.5):
    correct = 0
    for d in data:
        value = 1 if d[2] > threshold else 0
        if value == d[0]:
            correct += 1
    return [correct, len(data), correct/len(data)*100]

def statistics(data, threshold=0.5):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for d in data:
        value = 1 if d[2] > threshold else 0
        if value == d[0]:
            if value == 1:
                tp += 1
            else:
                tn += 1
        else:
            if value == 1:
                fp += 1
            else:
                fn += 1
    return [tp, fp, tn, fn]

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

# BROKEN
def AP(predicted, real, k=-1):
    result = 0
    tp = 0

    if k < 0:
        k = len(real)

    for i in xrange(k):
        if predicted[i] == real[i] and real[i] == 1:
            tp += 1
            result += tp/(i+1)

    return result / min(k, tp)

AP([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 0, 1, 1, 1, 1, 0, 0, 0, 1], k=10)
AP([1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 0, 0, 1, 1, 1, 0, 1, 1], k=10)

