import numpy as np

train_data = np.load('train_data.npz')
extra_train_data = np.load('validation_data.npz')

new_train_data_x = np.array(list(train_data['X']) + list(extra_train_data['X']))
new_train_data_y = np.array(list(train_data['y']) + [i // 30 for i in range(300)])

np.savez('new_train_data.npz', X=new_train_data_x, y=new_train_data_y)