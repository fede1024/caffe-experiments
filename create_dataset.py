#!/usr/bin/python

from __future__ import division
import sys, os

CAFFE = '/home/federico/tmp/caffe/python'
# Set the right path to your model file and pretrained model
#MODEL_FILE = '/home/federico/tmp/caffe/examples/imagenet/imagenet_deploy.prototxt'
MODEL_FILE = '/home/federico/tmp/caffe/examples/imagenet/imagenet_1image.prototxt'
PRETRAINED = '/home/federico/tmp/caffe/examples/imagenet/caffe_reference_imagenet_model'

KEEP_RATIO = 1
EXT = ".jpg"
MODE = 'cpu'

if not os.path.exists(CAFFE):
    sys.exit('ERROR: Caffe library %s was not found!' % CAFFE)

sys.path.append(CAFFE)

if len(sys.argv) < 4:
    sys.exit('Usage: %s layer_name1 layer_name2 ... annotation_file input_dir output_dir' % sys.argv[0])

if not os.path.exists(MODEL_FILE):
    sys.exit('ERROR: Model file %s was not found!' % MODEL_FILE)

if not os.path.exists(PRETRAINED):
    sys.exit('ERROR: Trained network %s was not found!' % PRETRAINED)

import fileinput
from caffe import imagenet
import time
import random
from os import listdir
from os.path import isfile, join


layers = sys.argv[1:-3]
annotation_file = sys.argv[len(sys.argv)-3]
input_folder = sys.argv[len(sys.argv)-2]
output_folder = sys.argv[len(sys.argv)-1]

if not os.path.isdir(input_folder):
    sys.exit('ERROR: Input folder %s is not valid!' % input_folder)

if not os.path.isdir(output_folder):
    sys.exit('ERROR: Output folder %s is not valid!' % output_folder)

print "Loading network..."
start = time.time()

# WARNING: using center_only allows faster image processing, but the input
# dimension in the prototxt file must be 1 instead of 10
#net = imagenet.ImageNetClassifier(MODEL_FILE, PRETRAINED)
net = imagenet.ImageNetClassifier(MODEL_FILE, PRETRAINED, center_only=True)
print "Network loaded in in %.2fs\n"%(time.time() - start)

net.caffenet.set_phase_test()

if MODE == 'cpu':
    net.caffenet.set_mode_cpu()
else:
    net.caffenet.set_mode_gpu()

images = {}

with open(annotation_file, 'r') as file:
    for line in file:
        image_name, value = line.rstrip().split(" ")
        if value == "S":
            continue
        image_path = join(input_folder, image_name + EXT)
        if isfile(image_path) and random.random() < KEEP_RATIO:
            images[image_path] = 1 if value == "P" else 0

images_num = len(images)

print "Images:", images_num
print "Extracting data for layers %s:"%layers

layer_files = {}

for layer in layers:
    if layer in net.caffenet.blobs.keys():
        shape = net.caffenet.blobs[layer].data.shape
        print "  Layer %s dimensions: %s [%d values]"%(layer, shape, reduce(lambda x, y: x*y, shape))
        layer_files[layer] = open(output_folder + "/" + layer, "w+")
    else:
        print "  Layer %s does not exist. Layers:"%(layer), net.caffenet.blobs.keys()
        exit()

print "\nStarting image elaboration:"

count = 1

for image_path in sorted(images.keys()):
    image_name, ext = os.path.basename(image_path).split(".")

    if not os.path.exists(image_path):
        sys.exit('ERROR: Image %s was not found!' % image_path)

    start = time.time()
    prediction = net.predict(image_path)
    print "%3d%%\tImage: %s     \t%.2fs        \r"%(count/images_num*100, image_name, time.time() - start),
    sys.stdout.flush()

    for layer in layers:
        # TODO spiegare usare 4
        numbers = net.caffenet.blobs[layer].data[0].flatten().tolist()
        line = " ".join(["%d:%.2f"%(n+1,v) for n, v in enumerate(numbers) if v != 0])
        label = str(images[image_path])
        layer_files[layer].write(label + " " + line + " # " + image_name + " " + label + "\n")

    count += 1

for layer_file in layer_files.values():
    layer_file.close()

print "\nDONE"
