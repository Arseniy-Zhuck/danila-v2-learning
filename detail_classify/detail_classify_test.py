import os

import numpy as np
from tensorflow import keras
import cv2

model_loaded = keras.models.load_model('detail_classify/detail_classify_model_10000_50_16.h5')
mistakes = []
print('learning-dataset starts')
# test_res = []
n = 0
dir = 'detail_classify/dataset_10000/train/rama'
files = os.listdir(dir)
print('rama --- proccessing')
correct_answers = 0
for file in files:
    if (n>1):
        per_cent = correct_answers / float(n)
        print(str(n) + ' tests are ready - current percent ' + str(per_cent))
    whole_file_name = dir + '\\' + file
    img = cv2.imread(whole_file_name)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_size = cv2.resize(img_grey, (512, 512))
    data = np.array(img_grey_size, dtype="float") / 255.0
    data = data.reshape((1, 512, 512))
    res = model_loaded.predict(data)
    if res[0][0] > 0.5:
        correct_answers+=1
    else:
        mistakes.append('train rama ' + file)
    n+=1

dir = 'detail_classify/dataset_10000/train/vagon'
files = os.listdir(dir)
print('vagon --- proccessing')
for file in files:
    if n > 1:
        per_cent = correct_answers / float(n)
        print(str(n) + ' tests are ready - current percent ' + str(per_cent))
    whole_file_name = dir + '\\' + file
    img = cv2.imread(whole_file_name)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_size = cv2.resize(img_grey, (512, 512))
    data = np.array(img_grey_size, dtype="float") / 255.0
    data = data.reshape((1, 512, 512))
    res = model_loaded.predict(data)
    if res[0][0] < 0.5:
        correct_answers+=1
    else:
        mistakes.append('train vagon ' + file)
    n+=1


print('test-dataset starts')
# test_res = []
test_n = 0
dir = 'detail_classify/dataset_10000/test/rama'
files = os.listdir(dir)
print('rama --- proccessing')
test_correct_answers = 0
for file in files:
    if (test_n > 1):
        per_cent = test_correct_answers / float(test_n)
        print(str(test_n) + ' tests are ready - current percent ' + str(per_cent))
    whole_file_name = dir + '\\' + file
    img = cv2.imread(whole_file_name)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_size = cv2.resize(img_grey, (512, 512))
    data = np.array(img_grey_size, dtype="float") / 255.0
    data = data.reshape((1, 512, 512))
    res = model_loaded.predict(data)
    if res[0][0] > 0.5:
        test_correct_answers+=1
    else:
        mistakes.append('test rama ' + file)
    test_n+=1

dir = 'detail_classify/dataset_10000/test/vagon'
files = os.listdir(dir)
print('vagon --- proccessing')
for file in files:
    if (test_n > 1):
        per_cent = test_correct_answers / float(test_n)
        print(str(test_n) + ' tests are ready - current percent ' + str(per_cent))
    whole_file_name = dir + '\\' + file
    img = cv2.imread(whole_file_name)
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_grey_size = cv2.resize(img_grey, (512, 512))
    data = np.array(img_grey_size, dtype="float") / 255.0
    data = data.reshape((1, 512, 512))
    res = model_loaded.predict(data)
    if res[0][0] < 0.5:
        test_correct_answers+=1
    else:
        mistakes.append('test vagon ' + file)
    test_n+=1
m_n = 1
for mistake in mistakes:
    print(str(m_n) + '. ' + mistake)
    m_n += 1
per_cent = correct_answers / float(n)
print('learning-dataset' + str(n) + ' tests are ready - current percent ' + str(per_cent))
per_cent = test_correct_answers / float(test_n)
print('test-dataset' + str(test_n) + ' tests are ready - current percent ' + str(per_cent))