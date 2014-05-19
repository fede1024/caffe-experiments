#!/usr/bin/python

#
# Usage:  ./create_dataset labels imagenet_data output_dataset
#
# Takes as input the file with all the labels in association with images in
# python format (ar created with the combine_annotations.py script), and the
# data extracted with the extract_values.py script. It outputs a file in libsvm
# format.
#

import sys

if len(sys.argv) < 4:
    print "Usage: %s labels imagenet_data output_dataset"%sys.argv[0]
    sys.exit(1)

# If true, it keeps only the most frequent lable among the database, giving a
# single label per image.
#KEEP_ONE = False
KEEP_ONE = True

print "Opening labels file."

f = open(sys.argv[1], "r")
images = eval(f.read())
f.close()

labels = {}

for image_labels in images.values():
    for label in image_labels:
        count = labels.get(label, 0)
        labels[label] = count + 1

label_number = {}

for n, l in enumerate(sorted(list(labels))):
    label_number[l] = n+1 # Labels start from 1

print "Writing dataset file."

output_file = open(sys.argv[3], "w+")

count = 0

with open(sys.argv[2]) as data_file:
    for line in data_file:
        count += 1
        if count % 1000 == 0:
            print "Image n:", count
        data_line = line.split(" ")
        image_name = data_line[0]
        image_data = data_line[1:]
        if image_name not in images:
            continue
        if KEEP_ONE:
            image_labels = images[image_name]
            nums = [str(max([[label_number[l], labels[l]] for l in image_labels], key = lambda x: x[1])[0])]
        else:
            nums = [str(label_number[l]) for l in images[image_name]]
        vals = ["%d:%s"%(n+1,v) for n, v in enumerate(image_data) if v != "0"]
        output_file.write(",".join(nums) + " " + " ".join(vals))

