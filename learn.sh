#!/bin/bash

echo POOL 5
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/pool5.scaled train_out2/pool5

echo CONV 4
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/conv4.scaled train_out2/conv4

echo CONV 5
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/conv5.scaled train_out2/conv5

echo CONV 3
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/conv3.scaled train_out2/conv3

echo NORM 2
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/norm2.scaled train_out2/norm2

echo NORM 1
time ./plibsvm-3.18/svm-train -b 1 -t 1 -d 3 -c 32 -g 0.0078125 ds/Adult_02/train/norm1.scaled train_out2/norm1

