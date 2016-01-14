#!/usr/bin/python3
from __future__ import print_function
import numpy as np
from scipy import ndimage
from progressbar import *

from sklearn.ensemble import ExtraTreesClassifier, BaggingClassifier, VotingClassifier
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier

from sklearn.cross_validation import cross_val_score

import normal_image
import cv2
from scipy import ndimage

def test_classifier(cl, train_x, train_y):
    print('Train accuracy: ', cl.score(train_x, train_y))
    print('Cross-validation accuracy: ', cross_val_score(cl, train_x, train_y, cv=10).mean())


train_data = np.load('new_train_data.npz')
validation_data = np.load('test_data_public.npz')

a = {0: 0,
     1: 0,
     2: 0,
     3: 0,
     4: 0,
     5: 0,
     6: 0,
     7: 0,
     8: 0,
     9: 0}

for digit in train_data['y']:
    a[digit] += 1


print(a)
print("size: ", len(train_data['y']))

fin = open('bad_samples.txt', 'w')
fin.close()

new_train_x = train_data['X'][1950:].copy()
new_train_y = train_data['y'][1950:].copy()

widgets = ['Processing train data: ', Percentage(), ' ',
            Bar(marker='>', left='[', right=']'),
            ' ', ETA(), ' ', FileTransferSpeed()]

pbar = ProgressBar(widgets=widgets, maxval=len(new_train_x))
pbar.start()

for i in range(len(new_train_x)):
    n = normal_image.NormalImage(new_train_x[i].copy())
    n.smooth()
    new_train_x[i] = n.get_np_array()

    pbar.update(i)

pbar.finish()


cl = OneVsRestClassifier(ExtraTreesClassifier(n_estimators=2000, min_samples_split=1, n_jobs=-1))

cl.fit(new_train_x, new_train_y)
test_classifier(cl, new_train_x, new_train_y)


validation_data_x = validation_data['X'].copy()

widgets = ['Processing validation data: ', Percentage(), ' ',
            Bar(marker='>', left='[', right=']'),
            ' ', ETA(), ' ', FileTransferSpeed()]

pbar = ProgressBar(widgets=widgets, maxval=len(validation_data_x))
pbar.start()

with open('bad_samples.txt', 'a') as fin:
    fin.write('VALIDATION NOW\n')

for i in range(len(validation_data_x)):
    n = normal_image.NormalImage(validation_data_x[i])
    n.smooth()
    validation_data_x[i] = n.get_np_array()

    pbar.update(i)

pbar.finish()


fout = open('answer.csv', 'w')
fout.write('id,answer\n')

i = 0

widgets = ['Predicting: ', Percentage(), ' ',
            Bar(marker='>', left='[', right=']'),
            ' ', ETA(), ' ', FileTransferSpeed()]

pbar = ProgressBar(widgets=widgets, maxval=len(validation_data_x))
pbar.start()

for pr in cl.predict(validation_data_x):
    fout.write('%d,%d\n' % (i, pr))
    pbar.update(i)
    i += 1

pbar.finish()
fout.close()
