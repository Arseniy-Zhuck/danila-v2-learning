from data_classes.letters_in_image import Letters_In_Image, Yolo_label_Rect, Letter_In_Image

import json

import torch
import cv2
import os

from word_compare_result import Word_compare_result

# model and dataset
model_path = 'models/letters-detect/06_05_1000_764_n_1500/exp13/weights/best.pt'
dir_path = 'letters-detect/words_test/ruzhimmash/'
label_path = dir_path + 'year.txt'
image_dir_path = dir_path + 'year'
test_results = 'letters-detect/words_test_results/ruzhimmash_year_exp13.txt'
str1 = 'model - 06_05_1000_764_n_1500/exp13/weights/best.pt\nruzhimmash_year\n'


# useful addresses
yolo_path = 'yolov5'
image_dir = os.listdir(image_dir_path)
model = torch.hub.load(yolo_path, 'custom', model_path, source='local')

counts = {Word_compare_result.equal:0,Word_compare_result.partial:0,Word_compare_result.none:0,Word_compare_result.wrong:0}
per_cents = {Word_compare_result.equal:0.0,Word_compare_result.partial:0.0,Word_compare_result.none:0.0,Word_compare_result.wrong:0.0}
new_lines = []
data = {}
with open(label_path) as f:
    for line in f:
        lst = line.split()
        data[lst[0]] = lst[1]

new_lines.append(str1)
print(str1)
for image_name in image_dir:
    img_path = image_dir_path + '/' + image_name
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    size_h = int(round(h / 32.0)) * 32
    size_w = int(round(w / 32.0)) * 32
    results = model([img_path], size = (h,w))
    json_res = results.pandas().xyxy[0].to_json(orient="records")
    res2 = json.loads(json_res)
    img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
    img_letters.sort_letters()
    img_letters.delete_intersections()
    # label_path = label_dir_path + '/' + image_name.split('.')[0] + '.txt'
    label_letters = Letters_In_Image()
    d = data[image_name.split('.')[0]]
    for letter in d:
        label_letters.letters.append(Letter_In_Image(letter))
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
