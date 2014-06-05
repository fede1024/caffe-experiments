#!/bin/bash

echo 1
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/conv3 > ds/Bus_005/train/conv3.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/conv3 > ds/Bus_005/test/conv3.scaled

echo 2
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/conv4 > ds/Bus_005/train/conv4.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/conv4 > ds/Bus_005/test/conv4.scaled

echo 3
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/conv5 > ds/Bus_005/train/conv5.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/conv5 > ds/Bus_005/test/conv5.scaled

echo 4
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/pool5 > ds/Bus_005/train/pool5.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/pool5 > ds/Bus_005/test/pool5.scaled

echo 5
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/norm2 > ds/Bus_005/train/norm2.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/norm2 > ds/Bus_005/test/norm2.scaled

echo 6
./plibsvm-3.18/svm-scale -s tmp_scale -l 0 ds/Bus_005/train/norm1 > ds/Bus_005/train/norm1.scaled
./plibsvm-3.18/svm-scale -r tmp_scale -l 0 ds/Bus_005/test/norm1 > ds/Bus_005/test/norm1.scaled
