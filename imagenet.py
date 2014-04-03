#!/usr/bin/python

import sys, os

CAFFE = '/home/federico/tmp/caffe/python'

if not os.path.exists(CAFFE):
    sys.exit('ERROR: Caffe library %s was not found!' % CAFFE)

sys.path.append(CAFFE)

from caffe import imagenet
#from matplotlib import pyplot
import time

# Set the right path to your model file, pretrained model,
# and the image you would like to classify.
MODEL_FILE = '../models/imagenet.prototxt'
PRETRAINED = '../models/caffe_reference_imagenet_model'
SYNSET = './synset'

MODE = 'cpu'

if len(sys.argv) < 2:
    sys.exit('Usage: %s image1 image2 ...' % sys.argv[0])

if not os.path.exists(MODEL_FILE):
    sys.exit('ERROR: Model file %s was not found!' % MODEL_FILE)

if not os.path.exists(PRETRAINED):
    sys.exit('ERROR: Trained network %s was not found!' % PRETRAINED)

if not os.path.exists(SYNSET):
    sys.exit('ERROR: Synset network %s was not found!' % SYNSET)

print "Loading network..."
start = time.time()
net = imagenet.ImageNetClassifier(MODEL_FILE, PRETRAINED)
print "Loaded in %.2fs"%(time.time() - start)

net.caffenet.set_phase_test()

if MODE == 'cpu':
    net.caffenet.set_mode_cpu()
else:
    net.caffenet.set_mode_gpu()

# Opening synset
with open(SYNSET) as f:
    synset = [line.strip() for line in f]

for IMAGE_FILE in sys.argv[1:]:
    print "\nImage:", IMAGE_FILE
    if not os.path.exists(IMAGE_FILE):
        sys.exit('ERROR: Image %s was not found!' % IMAGE_FILE)

    start = time.time()
    prediction = net.predict(IMAGE_FILE)
    print "Prediction time: %.2fs"%(time.time() - start)
    #pyplot.plot(prediction)

    results = sorted([[i, p] for i, p in enumerate(prediction)],
                    key=lambda p: -p[1])[0:5]

    for n, [index, value] in enumerate(results):
        print "%d) %d %.3f %s"%(n+1, index, value, synset[index])

    #pyplot.show()

