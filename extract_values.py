#!/usr/bin/python

from __future__ import division
import sys, os
import fileinput

CAFFE = '/home/federico/tmp/caffe/python'

if not os.path.exists(CAFFE):
    sys.exit('ERROR: Caffe library %s was not found!' % CAFFE)

sys.path.append(CAFFE)

from caffe import imagenet
import time
from os import listdir
from os.path import isfile, join

KEEP_RATIO = 0.1
EXT = ".jpg"

# Set the right path to your model file and pretrained model
#MODEL_FILE = '/home/federico/tmp/caffe/examples/imagenet/imagenet_deploy.prototxt'
MODEL_FILE = '/home/federico/tmp/caffe/examples/imagenet/imagenet_1image.prototxt'
PRETRAINED = '/home/federico/tmp/caffe/examples/imagenet/caffe_reference_imagenet_model'

MODE = 'cpu'

if len(sys.argv) < 4:
    sys.exit('Usage: %s layer_name1 layer_name2 ... annotation_file input_dir output_dir' % sys.argv[0])

if not os.path.exists(MODEL_FILE):
    sys.exit('ERROR: Model file %s was not found!' % MODEL_FILE)

if not os.path.exists(PRETRAINED):
    sys.exit('ERROR: Trained network %s was not found!' % PRETRAINED)

layers = sys.argv[1:-3]
annotation = sys.argv[len(sys.argv)-3]
input_folder = sys.argv[len(sys.argv)-2]
output_folder = sys.argv[len(sys.argv)-1]

if not os.path.isdir(output_folder):
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
        if random.random() < KEEP_RATIO:
            images[image_path] = 1 if value == "N" else 1

print "Images:", len(images)
print "Extracting data for layers %s:"%layers

layer_files = {}

for layer in layers:
    if layer in net.caffenet.blobs.keys():
        print "  Layer %s dimensions:"%(layer), net.caffenet.blobs[layer].data.shape
        layer_files[layer] = open(output_folder + "/" + layer, "w+")
    else:
        print "  Layer %s does not exist. Layers:"%(layer), net.caffenet.blobs.keys()
        exit()

print "\nStarting image elaboration:"

count = 1

for image_path in image.keys:
    image_name, ext = os.path.basename(image_path).split(".")
    sys.stdout.flush()

    if not os.path.exists(image_path):
        sys.exit('ERROR: Image %s was not found!' % image_path)

    start = time.time()
    prediction = net.predict(image_path)
    print "%3d%%\tImage: %s %.2fs"%(count/images_num*100, image_name, time.time() - start)

    for layer in layers:
        # TODO spiegare usare 4
        numbers = net.caffenet.blobs[layer].data[0].flatten().tolist()
        line = image_name + " " + " ".join(["0" if n == 0 else "%.3f"%n for n in numbers]) + "\n"
        layer_files[layer].write(line)

    count += 1

for layer_file in layer_files.values():
    layer_file.close()

print "\nDONE"
