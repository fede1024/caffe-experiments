#!/usr/bin/python

from __future__ import division
import sys
import pprint
import random
from os import listdir
from os.path import isdir, isfile, join
import shutil

KEEP=0.5

if len(sys.argv) < 4:
    print "Usage: %s ann_folder input_dataset output_Dataset "%(sys.argv[0])
    sys.exit(1)

def list_files(path):
    return [f for f in listdir(path) if isfile(join(path,f)) ]

ann_path = sys.argv[1]
in_path = sys.argv[2]
out_path = sys.argv[3]

if not isdir(ann_path):
    sys.exit('ERROR: Annotation folder %s is not valid!' % ann_folder)

if not isdir(in_path):
    sys.exit('ERROR: Input folder %s is not valid!' % in_folder)

if not isdir(out_path):
    sys.exit('ERROR: Output folder %s is not valid!' % out_folder)

images = set()
images_all = set()
files_list = sorted(list_files(ann_path))

for annotation_file in files_list:
    annotation_name, ext = annotation_file.split(".")
    if ext != "ann":
        continue
    print "=>", annotation_name
    with open(join(ann_path, annotation_file), 'r') as file:
        for line in file:
            image_name, value = line.rstrip().split(" ")
            images_all.add(image_name)
            if value != "P":
                continue
            images.add(image_name)


print "\nCopying files...\r"
sys.stdout.flush()

# Some images may not exist (for example if we split our dataset in training
# and testing parts and then we reduce only one of the two).
found_c = 0

for img in images:
    try:
        if random.random() < KEEP:	
            shutil.copyfile(join(in_path, img + ".jpg"), join(out_path, img + ".jpg"))
            found_c += 1
    except IOError:
        pass

print "DONE"

print "\nStatistics:"
print "  Total images in annotations:", len(images_all)
print "  Positive labels:", len(images)
print "  Keep ratio:", KEEP
print "  Images found and copied:", found_c

