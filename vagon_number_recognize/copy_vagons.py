import os

import cv2

whole_dir = 'balka/initial_balkas/ruzhimmash'
work_dir = os.listdir(whole_dir)
index = 2698
for img_name in work_dir:
    whole_img_name = whole_dir + '/' + img_name
    img = cv2.imread(whole_img_name)
    cv2.imwrite('balka/initial_images/ruzhimmash/balka_' + str(index) + '.jpg', img)
    index += 1