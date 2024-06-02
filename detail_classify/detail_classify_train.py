#Подключаем библиотеки
import os

import cv2
import tensorflow as tf
# from keras.src.layers import Flatten
from tensorflow import keras
import numpy as np

import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
# from tensorflow.python.keras import Input
# from keras.models import Model
# from keras.layers import concatenate
# from keras.layers import Input, Convolution2D, MaxPooling2D, UpSampling2D

data = []
labels = []

new_dir = 'detail_classify/dataset/train/rama'
files = os.listdir(new_dir)
print(new_dir)
n = 1
for file in files:
    whole_file_name = new_dir + '\\' + file
    img = cv2.imread(whole_file_name)
    img_resize = cv2.resize(img,(512,512))
    img1 = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
    data.append(img1)
    labels.append(0)
    n+=1


new_dir = 'detail_classify/dataset/train/vagon'
files = os.listdir(new_dir)
print(new_dir)
for file in files:
    whole_file_name = new_dir + '\\' + file
    img2 = cv2.imread(whole_file_name)
    img_resize2 = cv2.resize(img2,(512,512))
    img3 = cv2.cvtColor(img_resize2, cv2.COLOR_BGR2GRAY)
    data.append(img3)
    labels.append(1)
    n+=1

data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)

(trainX, testX, trainY, testY) = train_test_split(data,
    labels, test_size=0.001, shuffle= True, random_state=42)

textY = keras.utils.to_categorical(testY, 2)
trainY = keras.utils.to_categorical(trainY, 2)

from keras import models, Input
from keras import layers

model = models.Sequential([
    layers.Conv2D(32, (3,3), activation='relu', # (3,3) - фильтр
                        input_shape=(512,512,1)),
    layers.MaxPooling2D((2,2)), # фильтр (2,2) для пулинга
    layers.Conv2D(64, (3,3), activation='relu'),
    layers.MaxPooling2D((2,2)),
    layers.Conv2D(128, (3,3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.Flatten(),
    layers.Dense(512, 'relu'),
    layers.Dense(256, 'relu'),
    layers.Dense(128, 'relu'),
    layers.Dense(64, 'relu'),
    layers.Dense(32, 'relu'),
    layers.Dense(16, 'relu'),
    layers.Dense(8, 'relu'),
    layers.Dense(2, 'softmax')
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.fit(trainX, trainY, epochs=50, batch_size=16)

model.save('detail_classify/detail_classify_model.h5')
model_loaded = keras.models.load_model('detail_classify/detail_classify_model.h5')

test_loss, test_acc = model_loaded.evaluate(testX, testY)

print(test_loss, test_acc)

