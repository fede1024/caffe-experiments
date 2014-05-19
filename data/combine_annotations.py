#!/usr/bin/python

#
# Open the annotation folder (input) and creates a list with images names and
# features, example:
#
#   shot11722_17_RKF Airplane, Sky
#   shot11882_01_RKF Adult
#   ...
#
# Only positive (P) annotation are used. Images that don't appear in any
# annotation file are ignored.
#
# Usage: image_features.py -p ann_folder output_file
#
# With -p the output will be a python structure, with -t a formatted text will
# be created.
#

from __future__ import division
import sys
import pprint
from os import listdir
from os.path import isfile, join

if len(sys.argv) < 4:
    print "Usage: %s -p|-t ann_folder output_file"%(sys.argv[0])
    sys.exit(1)

def list_files(path):
    return [f for f in listdir(path) if isfile(join(path,f)) ]

dir_path = sys.argv[2]
out_path = sys.argv[3]

images = {}
images_all = set()
files_list = sorted(list_files(dir_path))

labels = {}

for annotation_file in files_list:
    annotation_name, ext = annotation_file.split(".")
    if ext != "ann":
        continue
    print "=>", annotation_name
    with open(join(dir_path, annotation_file), 'r') as file:
        for line in file:
            image_name, value = line.rstrip().split(" ")
            images_all.add(image_name)
            if value != "P":
                continue
            feature_list = images.get(image_name, [])
            feature_list.append(annotation_name)
            images[image_name] = feature_list
            labels[annotation_name] = 1

print "\nWriting output on %s and %s_py..."%(out_path, out_path),
sys.stdout.flush()

if sys.argv[1] == "-t":
    with open(out_path, 'w+') as out:
        for image_name, feature_list in images.items():
            features_count += len(feature_list)
            out_str = image_name + " " + " ".join(feature_list) + "\n"
            out.write(out_str)
elif sys.argv[1] == "-p":
    with open(out_path, 'w+') as out:
        pp = pprint.PrettyPrinter()
        out.write("# Data structure in python format\n\n")
        out.write(pp.pformat(images) + "\n\n")
        for n, l in enumerate(sorted(list(labels))):
            out.write("#" + str(n+1) + " " + l + "\n")
else:
    print "Wrong parameter. Choose -p or -t."
    sys.exit(1)

print "DONE"


features_count = 0
features_combinations = set()
for image_name, feature_list in images.items():
    features_count += len(feature_list)
    features_combinations.add(tuple(feature_list))

print "\nStatistics:"
print "  Annotations:", len(files_list)
print "  Total images:", len(images_all)
print "  Images with annotations: %d (%d%%)"%(len(images), len(images)/len(images_all)*100)
print "  Average annotations per image: %.1f"%(features_count/len(images))
print "  Number of labels combinations:", len(features_combinations)