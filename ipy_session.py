# coding: utf-8
import numpy as np
import scipy.ndimage
import matplotlib.pyplot as plt
import cv2

def plot(a):
    plt.matshow(a, cmap=plt.get_cmap('Greys'))

get_ipython().magic(u'matplotlib inline')
get_ipython().magic(u'cd RSML/')

from normal_image import *

data_valid = np.load("validation_data.npz")
data_train = np.load('train_data.npz')

def bin(img, index):
    for i in range(28):
        for j in range(28):
            if img[i][j] > index:
                img[i][j] = 255
            else:
                img[i][j] = 0

    return  img

def invert(img):
    for i in range(28):
        for j in range(28):
	    img[i][j] = 255 - img[i][j]

    return img

sample = data_train['X'][37].reshape(28, 28)
