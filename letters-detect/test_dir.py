from data_classes.letters_in_image import Letters_In_Image, Yolo_label_Rect, Letter_In_Image

import json

import torch
import cv2
import os

from word_compare_result import Word_compare_result

# model and dataset
model_path = 'models/letters-detect/12_05_16_500_r/exp24/weights/best.pt'
dir_path = 'letters-detect/ruzhimmash/dataset_500_r/test'
test_results = 'letters-detect/test_results/exp22_dataset_500_r_test.txt'
str1 = 'model_initial - none, trained_dataset - dataset_500_r, model - 12_05_16_500_r, test_dataset - 50 image \n'

# useful addresses
label_dir_path = dir_path + '/' + 'labels'
image_dir_path = dir_path + '/' + 'images'
yolo_path = 'yolov5'
image_dir = os.listdir(image_dir_path)
model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

counts = {Word_compare_result.equal:0,Word_compare_result.partial:0,Word_compare_result.none:0,Word_compare_result.wrong:0}
per_cents = {Word_compare_result.equal:0.0,Word_compare_result.partial:0.0,Word_compare_result.none:0.0,Word_compare_result.wrong:0.0}
new_lines = []

new_lines.append(str1)
for image_name in image_dir:
    img_path = image_dir_path + '/' + image_name
    results = model([img_path], size = 32)
    json_res = results.pandas().xyxy[0].to_json(orient="records")
    res2 = json.loads(json_res)
    img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
    img_letters.sort_letters()
    img_letters.delete_intersections()
    label_path = label_dir_path + '/' + image_name.split('.')[0] + '.txt'
    data = []
    with open(label_path) as f:
        for line in f:
            data.append([float(x) for x in line.split()])
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    label_letters = Letters_In_Image()
    for d in data:
        yolo_label_rect = Yolo_label_Rect.build_from_2D_array(d, h, w)
        rect_labeled = yolo_label_rect.build_rect()
        label_letters.letters.append(Letter_In_Image(str(int(d[0])), rect_labeled))
    label_letters.sort_letters()
    new_lines.append(img_letters.make_word() + ' - ' + label_letters.make_word())
    new_lines.append('\n')
    # if len(img_letters.letters) == len(label_letters.letters):
    #     flag = True
    #     for i in range(0, len(label_letters.letters)):
    #         flag = flag and (img_letters.letters[i].letter == label_letters.letters[i].letter)
    #     print(flag)
    # else:
    #     print(False)
    compare_result = Letters_In_Image.compare(img_letters, label_letters)
    counts[compare_result] += 1
print(counts)
new_lines.append(str(counts))
for (result,count) in counts.items():
    per_cents[result] = round(count / float(len(image_dir)), 3) * 100
print(per_cents)
new_lines.append('\n')
new_lines.append(str(per_cents))
with open(test_results, "w") as new_f:
    new_f.writelines(new_lines)
