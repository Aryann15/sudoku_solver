import numpy as np
import cv2 as cv
import os
import random
from sklearn.model_selection import train_test_split
from keras.preprocessing.image import ImageDataGenerator
from keras.utils.np_utils import to_categorical


path= 'data'
training_data = []

myList = os.listdir(path)
print(myList)

class_numbers = len(myList)
for x in range(0,class_numbers):
    pic_list = os.listdir(path + '/' + str(x))
    for y in pic_list:
        current_image = cv.imread(path+'/'+str(x)+ '/' +y)
        current_image = cv.resize(current_image,(32,32))
        training_data.append([current_image,class_numbers])
    print(x)

training_data = np.array(training_data, dtype=object)

print(len(training_data))

random.seed(10160)
random.shuffle(training_data)
for features, labels in training_data[:10]:
    print(labels)

X=[]
Y=[]

for features,labels in training_data:
    X.append(features)
    Y.append(labels)

X=np.array(X).reshape(-1,100,100,1)
X=X.astype('float32')
X=X/255

Y=np.array(Y)