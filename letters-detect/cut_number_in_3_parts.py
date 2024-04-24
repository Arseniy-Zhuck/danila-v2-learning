import os

import cv2


imgs_for_cut_dir = 'crops/number/'

files = os.listdir(imgs_for_cut_dir)
cut_number = 0
for img in files:
    whole_file_name = imgs_for_cut_dir + '\\' + img
    img = cv2.imread(whole_file_name)
    h, w = img.shape[:2]
    left_border = 0
    right_border = int(w / 3)
    for i in range(3):
        cut_number += 1
        left_border_cur = left_border
        right_border_cur = right_border
        # if (left_border_cur > 0):
        #     left_border_cur -= int(w / 16)
        # if (right_border_cur < w -1):
        #     right_border_cur -= int(w / 16)
        letter_img = img[0:h , left_border_cur:right_border_cur]
        cv2.imwrite('cuts/' + 'cut_' + str(cut_number) + '.jpg', letter_img)
        left_border = right_border
        right_border = left_border + int(w/3)