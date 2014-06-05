#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import time
#%matplotlib inline

# Make sure that caffe is on the python path:
import sys, os

CAFFE = '/home/federico/tmp/caffe/python'

if not os.path.exists(CAFFE):
    sys.exit('ERROR: Caffe library %s was not found!' % CAFFE)

sys.path.append(CAFFE)
import caffe
import caffe.imagenet

# Set the right path to your model file, pretrained model,
# and the image you would like to classify.
SYNSET = './synset'

#if len(sys.argv) < 2:
#    sys.exit('Usage: %s image1 image2 ...' % sys.argv[0])


if not os.path.exists(SYNSET):
    sys.exit('ERROR: Synset network %s was not found!' % SYNSET)

def load_network(model, network):
    if not os.path.exists(model):
        sys.exit('ERROR: Model file %s was not found!' % model)
    if not os.path.exists(network):
        sys.exit('ERROR: Trained network %s was not found!' % network)
    print "Loading network..."
    start = time.time()
    net = caffe.imagenet.ImageNetClassifier(model, network)
    #net = caffe.imagenet.ImageNetClassifier(model, network, num_output=256)
    #net = caffe.imagenet.ImageNetClassifier(model, network, center_only=True)
    print "Loaded in %.2fs"%(time.time() - start)
    return net

def set_mode(net, mode):
    if mode == 'cpu':
        net.caffenet.set_mode_cpu()
    else:
        net.caffenet.set_mode_gpu()

def print_blobs(blobs):
    for key in blobs:
        print "Blob %5s: num:%2d channels:%4d width:%3d height:%3d count:%s"%\
        (key, blobs[key].num, blobs[key].channels, blobs[key].width, blobs[key].height, blobs[key].count)

net = load_network('/home/federico/tmp/caffe/examples/imagenet/imagenet_deploy.prototxt', '/home/federico/tmp/caffe/examples/imagenet/caffe_reference_imagenet_model')
#net = load_network('/home/federico/tmp/caffe/models/my_imagenet.prototxt', '/home/federico/tmp/caffe/models/caffe_reference_imagenet_model')
set_mode(net, 'cpu')

net.caffenet.set_phase_test()

#scores = net.predict("/home/federico/tmp/images/lena.bmp")
scores = net.predict(sys.argv[1])

#print scores

#[(k, v.data.shape) for k, v in net.caffenet.blobs.items()]

blobs = net.caffenet.blobs
print_blobs(blobs)

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

def showimage(im):
    if im.ndim == 3:
        im = im[:, :, ::-1]
    plt.imshow(im)

# take an array of shape (n, height, width) or (n, height, width, channels)
#  and visualize each (height, width) thing in a grid of size approx. sqrt(n)
#  by sqrt(n)
def vis_square(data, padsize=1, padval=0):
    data -= data.min()
    data /= data.max()

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    showimage(data)


# 4 central one
# 9 central one mirrored
image_no = 4

# The input image
# index four is the center crop
image = net.caffenet.blobs['data'].data[image_no].copy()
image -= image.min()
image /= image.max()
showimage(image.transpose(1, 2, 0))

plt.show()

# The first layer filters, conv1
# the parameters are a list of [weights, biases]
filters = net.caffenet.params['conv1'][0].data
vis_square(filters.transpose(0, 2, 3, 1))
plt.show()

# The first layer output, conv1 (rectified responses of the filters above,
# first 36 only)
filters = net.caffenet.blobs['conv1'].data[0, :36]
vis_square(filters, padval=1)
plt.show()

# The second layer filters, conv2
# There are 128 filters, each of which has dimension 5 x 5 x 48.
# We show only the first 48 filters, with each channel shown separately,
# so that each filter is a row.
#filters = net.caffenet.params['conv2'][0].data
#vis_square(filters[:48].reshape(48**2, 5, 5))
#plt.show()

filters = net.caffenet.blobs['conv5'].data[image_no, 50:114]
vis_square(filters, padval=1)
plt.show()

#v = [[0 for x in xrange(0, 13)] for j in xrange(0, 13)]
v = np.zeros((13, 13))

m = 0
for x in xrange(0, 13):
    for y in xrange(0, 13):
        s = 0
        for filter_n in xrange(0, 255):
            s += net.caffenet.blobs['conv5'].data[image_no][filter_n][x][y]
        m = max(s, m)
        v[x][y] = s

for x in xrange(0, 13):
    for y in xrange(0, 13):
        v[x][y] /= m

showimage(v)
plt.show()

showimage(net.caffenet.blobs['conv5'].data[image_no][240])
plt.show()

showimage(net.caffenet.blobs['pool5'].data[image_no][240])
plt.show()
