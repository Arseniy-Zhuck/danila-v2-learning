import os

import albumentations as A
import cv2

transform = A.Compose([
    A.HorizontalFlip(p=0.8),
    A.ShiftScaleRotate(border_mode=cv2.BORDER_CONSTANT,
                          scale_limit=0.1,
                          rotate_limit=45,
                          p=0.5),
    A.RandomBrightnessContrast(brightness_limit=0.5, contrast_limit=0.5, p=0.5)
], p=1)

count = 0
index = 0
directory = 'detail_classify/dataset_1000/train/rama'
directory_way = 'detail_classify/dataset_10000/train/rama'
work_dir = os.listdir(directory)
for file_name in work_dir:
    index += 1
    image_path = directory + '/' + file_name
    image = cv2.imread(image_path)
    print(str(index) + '. ' + file_name)
    for i in range(9):
        transformed = transform(image=image)
        image_transformed = transformed['image']
        new_file_name = str(i) + file_name.split('.')[0] + '.jpg'
        print(str(index) + '. ' + str(i) + '. ' + new_file_name)
        cv2.imwrite(directory_way + '/' + new_file_name, image_transformed)
