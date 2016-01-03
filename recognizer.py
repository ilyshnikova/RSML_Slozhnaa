import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import cross_val_score
#import matplotlib.pyplot as plt
#import Image
import normal_image
import graph

def test_classifier(cl, train_x, train_y):
    print('Train accuracy: ', cl.score(train_x, train_y))
    print('Cross-validation accuracy: ', cross_val_score(cl, train_x, train_y, cv=10).mean())


BLACK = 255
WHITE = 0


train_data = np.load('train_data.npz')
validation_data = np.load('validation_data.npz')

#cl = KNeighborsClassifier()
#cl.fit(train_data['X'], train_data['y'])
#test_classifier(cl, train_data['X'], train_data['y'])

a = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

for i in range(0,len(train_data['X'])):
    a[train_data['y'][i]] += 1;

print(a)
print(sum(a.values()))
print("size: ", len(train_data['X']))

index = 0
for i in range(0, 10):
#    print i
#    print index
    index += a[i]

print(index)




#new_train_x = train_data['X'][0 : 30].copy()
#new_train_y = train_data['y'][0 : 30].copy()

#new_train_x = []
#new_train_y = []



#print(new_train_x)
#print(type(new_train_x))

index = 0
for i in range(0, 10):
#    print("fom ", index, " to ", index - 30

#    print(new_train_x)
#    print(len(new_train_x))
#    new_train_x = np.vstack([new_train_x, train_data['X'][index:index + 30].copy()])
#    new_train_y = np.vstack([new_train_y, train_data['y'][index:index + 30].copy()])


#    print(new_train_x)
#    print(len(new_train_x))

#    for j in  range(0, 30):
#        new_train_x.append(train_data['X'][index + j].copy())
#        new_train_y.append(train_data['y'][index + j].copy())

#       new_train_x = np.vstack([new_train_x, train_data['X'][index + j].copy()])
#       new_train_y = np.vstack([new_train_y, train_data['y'][index + j].copy()])

#        print "j", j
#        print index + j
#        train_data['X'][index + j]
#        print new_train_y
#        new_train_x = np.append([new_train_x], [train_data['X'][index + j].copy()])
#        new_train_y = np.append([new_train_y], train_data['y'][index + j].copy())
#
#           print new_train_y

    index += a[i]

#print(new_train_x)
#print(new_train_y)

new_train_x = train_data['X'][1950:].copy()
new_train_y = train_data['y'][1950:].copy()


#print(new_train_x)
#print(new_train_y)

cl = KNeighborsClassifier()
cl.fit(new_train_x, new_train_y)
test_classifier(cl, new_train_x, new_train_y)




for i in range(0, len(new_train_x)):
    n = normal_image.Normal_image(new_train_x[i])

    n.smooth()
    n.smooth()
    new_train_x[i] = n.get_np_array()




cl = KNeighborsClassifier()
cl.fit(new_train_x, new_train_y)
test_classifier(cl, new_train_x, new_train_y)

nvalidation_data_x = validation_data['X'].copy()
validation_data_x = validation_data['X'].copy()

for i in range(0, len(validation_data_x)):
    n = normal_image.Normal_image(validation_data_x[i])
    nvalidation_data_x[i] = n.image.reshape(28*28)
    n.smooth()
    validation_data_x[i] = n.get_np_array()


print(validation_data_x)

fout = open('answer.csv', 'w')
fout.write('id,answer\n')


count = 0
i = 0
for pr in cl.predict(validation_data_x):
    im = validation_data_x[i].reshape(28, 28)
    print("----------------------------")
    for x in range(0, 28):
        for y in range(0,28):
            if (im[x][y] == BLACK):
                print("X ", end="")
            else:
                print(". ", end="")


        print("")
    print("----------------------------")

#    n = normal_image.Normal_image(validation_data_x[i])
#    n.smooth()

    print(pr)
    if (int((i) / 2) == pr):
        count += 1

    fout.write('%d,%d\n' % (i, pr))
    i += 1

fout.close()

print("count : ", count)

#fout = open('answer1.csv', 'w')
#fout.write('id,answer\n')
#
#i = 0
#for pr in cl.predict(nvalidation_data_x):
##    n = normal_image.Normal_image(nvalidation_data_x[i])
##    n.smooth()
#
#
#    im = validation_data_x[i].reshape(28, 28)
#    print("----------------------------")
#    for x in range(0, 28):
#        for y in range(0,28):
#            if (im[x][y] == BLACK):
#                print("X ", end="")
#            else:
#                print(". ", end="")
#
#
#        print("")
#    print("----------------------------")
#
#    print(pr)
#
#    fout.write('%d,%d\n' % (i, pr))
#    i += 1
#
#fout.close()
#
