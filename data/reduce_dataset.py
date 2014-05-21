#!/usr/bin/python

from __future__ import division
import sys
import pprint
import random
from os import listdir, makedirs
from os.path import isdir, isfile, join, exists, basename
import shutil

KEEP_RATIO = 0.1
EXT = ".jpg"

if len(sys.argv) < 3:
    print "Usage: %s ann_file train_folder test_folder"%(sys.argv[0])
    sys.exit(1)

def list_files(path):
    return [f for f in listdir(path) if isfile(join(path,f)) ]

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

out_path_train = join(train_path,  "..", annotation_name + "_train")
if not exists(out_path_train):
    makedirs(out_path_train)

out_path_test = join(test_path, "..", annotation_name + "_test")
if not exists(out_path_test):
    makedirs(out_path_test)

print "New train folder:", out_path_train
print "New test folder:", out_path_test

counts = {"P_tr": 0, "N_tr": 0, "P_tr_c": 0, "N_tr_c": 0, "P_te": 0, "N_te": 0, "P_te_c": 0, "N_te_c": 0}
counts_train = {"P": 0, "N": 0, "S": 0}
counts_test = {"P": 0, "N": 0, "S": 0}
copied = 0

print "\nCopying files...\r"
sys.stdout.flush()

with open(ann_path, 'r') as file:
    for line in file:
        image_name, value = line.rstrip().split(" ")
        if value == "S":
            continue
        train_img = join(train_path, image_name + EXT)
        test_img = join(test_path, image_name + EXT)
        copied += 1
        if isfile(train_img):
            counts[value + "_tr"] += 1
            if random.random() < KEEP_RATIO:
                shutil.copyfile(train_img, join(out_path_train, image_name + EXT))
                counts[value + "_tr_c"] += 1
        elif isfile(test_img):
            counts[value + "_te"] += 1
            if random.random() < KEEP_RATIO:
                shutil.copyfile(test_img, join(out_path_test, image_name + EXT))
                counts[value + "_te_c"] += 1
        else:
            print "Image %s does not exist."%image_name

print "DONE"

print "\nStatistics:"
print "  Total images in annotations:", sum(counts.values())
print "  Positive images: %d (train: %d, test: %d)"%(counts["P_tr"] + counts["P_te"], counts["P_tr"], counts["P_te"])
print "  Negative images: %d (train: %d, test: %d)"%(counts["N_tr"] + counts["N_te"], counts["N_tr"], counts["N_te"])
print "  Keep ratio:", KEEP_RATIO
print "  Images copied: %d (train: %d, test: %d)"%(counts["P_tr_c"] + counts["P_te_c"] + counts["N_tr_c"] + counts["N_te_c"],
                                                    counts["P_te_c"] + counts["N_tr_c"], counts["P_te_c"] + counts["N_te_c"])

