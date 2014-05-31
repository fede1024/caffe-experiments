#!/usr/bin/python

from __future__ import division
import sys


def gen_ranking(data, k, threshold=0.5):
    data_s = sorted(data, key=lambda x: -x[3]) # sort by probability to be true

    relevant = set()
    ranking = []

    for n, real, p0, p1 in data_s:
        if real == 1:
            relevant.add(n)    # is a relevant document
        if p1 >= threshold:
            ranking.append(n)  # is in ranking

    return ranking[:k], relevant

def APK(data, k, threshold=0.5):
    ranking, relevants = gen_ranking(data, k, threshold=threshold)
    n = len([d for d in ranking if d in relevants])
    print "  Retrived documents:", len(ranking)
    print "  Relevant documents:", len(relevants)
    print "  Relevant retrived:", n
    return apk(relevants, ranking, len(ranking))

def calc_classification(data, threshold=0.5):
    correct = 0
    for d in data:
        value = 1 if d[3] >= threshold else 0
        if value == d[1]:
            correct += 1
    return [correct, len(data), correct/len(data)*100]

def statistics(data, threshold=0.5):
    tp = 0
    fp = 0
    tn = 0
    fn = 0
    for d in data:
        value = 1 if d[3] >= threshold else 0
        if value == d[1]:
            if value == 1:
                tp += 1
            else:
                tn += 1
        else:
            if value == 1:
                fp += 1
            else:
                fn += 1
    return {"tp": tp, "fp": fp, "tn": tn, "fn": fn, "class_acc": (tp+tn)/(tp+tn+fp+fn),
            "prec": tp/(tp+fp), "recall":tp/(tp+fn)}

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
            data.append([counter, int(data_line.split(" ")[0]), float(prob[1]), float(prob[2])])
            counter += 1
    stats = statistics(data, threshold=float(sys.argv[4]))
    print "STATS:"
    print "  TP: %3d  TN: %3d"%(stats["tp"], stats["tn"])
    print "  FP: %3d  FN: %3d"%(stats["fp"], stats["fn"])
    print "  Classification accuracy: %.2f%%"%(stats["class_acc"]*100)
    print "  Precision: %.2f%%"%(stats["prec"]*100)
    print "  Recall: %.2f%%"%(stats["recall"]*100)
    print "AVERAGE PRECISION:"
    ap = APK(data, int(sys.argv[3]), threshold=float(sys.argv[4]))
    print "  Average precision: %.3f"%ap

