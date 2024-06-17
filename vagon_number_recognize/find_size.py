import os

import cv2

h_over_w_summ = 0
h_sum = 0
w_sum = 0
count = 0
dir = 'vagon_number_recognize/dataset_9000/train/images'
files = os.listdir(dir)
for file in files:
    whole_file_name = dir + '\\' + file
    img = cv2.imread(whole_file_name)
    h, w = img.shape[:2]
    # h_over_w = h / float(w)
    # h_over_w_summ += h_over_w
    h_sum += h
    w_sum += w
    count += 1
# h_over_w_average = h_over_w_summ / float(count)
h_av = h_sum / float(count)
w_av = w_sum / float(count)
print('h_av = ' + str(h_av) + ', w_aw = ' + str(w_av))