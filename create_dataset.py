#!/usr/bin/python

import sys

print "Opening labels file."

f = open(sys.argv[1], "r")
images = eval(f.read())
f.close()

labels = set()
for image_labels in images.values():
    labels = labels.union(set(image_labels))

label_number = {}

for n, l in enumerate(sorted(list(labels))):
    label_number[l] = n+1 # Labels start from 1

print "Opening data file."

output_file = open(sys.argv[3], "w+")

count = 0

with open(sys.argv[2]) as data_file:
    for line in data_file:
        count += 1
        if count % 100 == 0:
            print "Image n:", count
        data_line = line.split(" ")
        image_name = data_line[0]
        image_data = data_line[1:]
        if image_name not in images:
            continue
        nums = [str(label_number[l]) for l in images[image_name]]
        vals = ["%d:%s"%(n+1,v) for n, v in enumerate(image_data) if v != "0"]
        output_file.write(",".join(nums) + " " + " ".join(vals))

