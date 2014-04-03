import sys
sys.path.append("/home/federico/tmp/caffe/python")

from caffe import imagenet
from matplotlib import pyplot

# Set the right path to your model file, pretrained model,
# and the image you would like to classify.
MODEL_FILE = '../models/imagenet.prototxt'
PRETRAINED = '../models/caffe_reference_imagenet_model'
IMAGE_FILE = '/home/federico/tmp/images/lena.bmp'

net = imagenet.ImageNetClassifier(MODEL_FILE, PRETRAINED)

net.caffenet.set_phase_test()
net.caffenet.set_mode_cpu()

prediction = net.predict(IMAGE_FILE)
#print 'prediction shape:', prediction.shape
pyplot.plot(prediction)

best = sorted([[i, p] for i, p in enumerate(prediction)],
              key=lambda p: -p[1])[0:5]

print best

pyplot.show()

