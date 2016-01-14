from scipy import ndimage
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import os
import sys
from progressbar import *

from normal_image import *


def filter(img):
    img_n = NormalImage(img, 1)
    img_n.smooth()

    return img_n.get_np_array().reshape(28, 28)

def filter_med(img):
    img_blur = ndimage.minimum_filter(img, 2)
    img_max = ndimage.maximum_filter(img, 2)
    return img_max.copy()


os.system("rm -f ./" + sys.argv[1] + "/*")
data_valid = np.load("validation_data.npz")
data_train = np.load('train_data.npz')


widgets = ['Processing images: ', Percentage(), ' ', Bar(marker='>', left='[', right=']'),
           ' ', ETA(), ' ', FileTransferSpeed()]

pbar = ProgressBar(widgets=widgets, maxval=len(data_valid['X']))
pbar.start()

for i in range(len(data_valid['X'])):
    img = data_valid['X'][i].reshape(28, 28)
    img_flt = filter_med(img.copy())

    mpimg.imsave('./' + sys.argv[1] + '/img' + str(i) + '_in.png', img, cmap=plt.get_cmap("Greys"))
    mpimg.imsave('./' + sys.argv[1] + '/img' + str(i) + '_out.png', img_flt, cmap=plt.get_cmap("Greys"))
    pbar.update(i)

pbar.finish()
