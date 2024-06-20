import os

import cv2

whole_dir = 'balka_photos/initial_balkas/bvrz'
work_dir = os.listdir(whole_dir)
index = 18334
for img_name in work_dir:
    whole_img_name = whole_dir + '/' + img_name
    img = cv2.imread(whole_img_name)
    cv2.imwrite('balka_photos/initial_images/bvrz/balka_' + str(index) + '.jpg', img)
    if (index % 100) == 0:
        print('balka_photos/initial_images/bvrz/balka_' + str(index) + '.jpg')
    index += 1