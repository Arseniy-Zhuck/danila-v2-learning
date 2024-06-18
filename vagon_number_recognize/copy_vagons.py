import os

import cv2

whole_dir = 'vagon_number_recognize/new_vagons/photos'
work_dir = os.listdir(whole_dir)
index = 0
for img_name in work_dir:
    whole_img_name = whole_dir + '/' + img_name
    img = cv2.imread(whole_img_name)
    cv2.imwrite('vagon_number_recognize/new_vagons/dataset/vagon_' + str(index) + '.jpg', img)
    index += 1