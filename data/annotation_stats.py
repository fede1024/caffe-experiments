#!/usr/bin/python

from __future__ import division
import sys
import pprint
import random
from os.path import isdir, isfile, join, exists, basename
import shutil

EXT = ".jpg"

if len(sys.argv) < 3:
    print "Usage: %s ann_file train_folder test_folder"%(sys.argv[0])
    sys.exit(1)

ann_path = sys.argv[1]
train_path = sys.argv[2]
test_path = sys.argv[3]

if not isfile(ann_path):
    sys.exit('ERROR: Annotation file %s is not valid!' % ann_path)

if not isdir(train_path):
    sys.exit('ERROR: Input folder %s is not valid!' % train_path)

if not isdir(test_path):
    sys.exit('ERROR: Input folder %s is not valid!' % test_path)

annotation_name, ext = basename(ann_path).split(".")

if ext != "ann":
    print "Annotation file is not valid."
    sys.exit(0)

counts = {"P_tr": 0, "N_tr": 0, "P_tr_c": 0, "N_tr_c": 0, "P_te": 0, "N_te": 0, "P_te_c": 0, "N_te_c": 0}
counts_train = {"P": 0, "N": 0, "S": 0}
counts_test = {"P": 0, "N": 0, "S": 0}

with open(ann_path, 'r') as file:
    for line in file:
        image_name, value = line.rstrip().split(" ")
        if value == "S":
            continue
        train_img = join(train_path, image_name + EXT)
        test_img = join(test_path, image_name + EXT)
        if isfile(train_img):
            counts[value + "_tr"] += 1
        elif isfile(test_img):
            counts[value + "_te"] += 1
        else:
            print "Image %s does not exist."%image_name

print "Statistics on %s:"%annotation_name
print "  Total images in annotations:", sum(counts.values())
print "  Positive images: %d (train: %d, test: %d)"%(counts["P_tr"] + counts["P_te"], counts["P_tr"], counts["P_te"])
print "  Negative images: %d (train: %d, test: %d)"%(counts["N_tr"] + counts["N_te"], counts["N_tr"], counts["N_te"])

