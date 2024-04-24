import os

import cv2

imgs_for_cut_dir = 'crops/year/'

files = os.listdir(imgs_for_cut_dir)
cut_number = 4157
for file in files:
    whole_file_name = imgs_for_cut_dir + '\\' + file
    img = cv2.imread(whole_file_name)
    cut_number += 1
    cv2.imwrite('cuts/' + 'cut_' + str(cut_number) + '.jpg', img)
