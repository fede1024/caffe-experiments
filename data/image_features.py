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
# Usage: image_features.py ann_folder output_file
#
# Another file called output_file_py is created, with output in python
# data structure.
#

from __future__ import division
import sys
import pprint
from os import listdir
from os.path import isfile, join

if len(sys.argv) < 3:
    print "Usage: %s ann_folder output_file"%(sys.argv[0])
    sys.exit(1)

def list_files(path):
    return [f for f in listdir(path) if isfile(join(path,f)) ]

dir_path = sys.argv[1]
out_path = sys.argv[2]

images = {}
images_all = set()
files_list = sorted(list_files(dir_path))

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

print "\nWriting output on %s and %s_py..."%(out_path, out_path),
sys.stdout.flush()

features_count = 0

with open(out_path, 'w+') as out:
    for image_name, feature_list in images.items():
        features_count += len(feature_list)
        out_str = image_name + " ".join(feature_list) + "\n"
        out.write(out_str)

with open(out_path + "_py", 'w+') as out:
    pp = pprint.PrettyPrinter()
    out.write("# Data structure in python format\n\n")
    out.write(pp.pformat(images))

print "DONE"

print "\nStatistics:"
print "  Annotations:", len(files_list)
print "  Total images:", len(images_all)
print "  Images with annotations: %d (%d%%)"%(len(images), len(images)/len(images_all)*100)
print "  Average annotations per image: %.1f"%(features_count/len(images))
