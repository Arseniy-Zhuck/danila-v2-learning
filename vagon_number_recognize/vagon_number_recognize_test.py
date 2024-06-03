import json

import torch
import cv2
import os

from vagon_number_recognize.Vagon_number_recognize_class import Vagon_number_recognize_class
from word_compare_result import Word_compare_result

# model and dataset
dir_path = 'vagon_number_recognize/dataset/'
label_path = dir_path + 'numbers.txt'
image_dir_path = dir_path + 'numbers'
test_results = 'vagon_number_recognize/test_results/easyocr_danila_189.txt'

# useful addresses
image_dir = os.listdir(image_dir_path)
vagon_number_recognizer = Vagon_number_recognize_class()

def compare(result_text, label_text):
    if result_text == '':
        return Word_compare_result.none
    elif result_text == label_text:
        return Word_compare_result.equal
    else:
        count_eq = 0
        index = 0
        while (index < len(label_text)) and (index < len(result_text)):
            if result_text[index] == label_text[index]:
                count_eq = count_eq + 1
            index += 1
        per_cent = float(count_eq) / len(label_text)
        if per_cent > 0.5:
            return Word_compare_result.partial
        else:
            return Word_compare_result.wrong


counts = {Word_compare_result.equal:0,Word_compare_result.partial:0,Word_compare_result.none:0,Word_compare_result.wrong:0}
per_cents = {Word_compare_result.equal:0.0,Word_compare_result.partial:0.0,Word_compare_result.none:0.0,Word_compare_result.wrong:0.0}
new_lines = []
data = {}
with open(label_path) as f:
    for line in f:
        lst = line.split()
        data[lst[0]] = lst[1]
n = 0
for image_name in image_dir:
    n += 1
    img_path = image_dir_path + '/' + image_name
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    result_text,_ = vagon_number_recognizer.work_image_cut(img_path)
    label_text = data[image_name]
    print(image_name)
    print(result_text + ' - ' + label_text)
    new_lines.append(str(n) + '. ' + image_name)
    new_lines.append('\n')
    new_lines.append(result_text + ' - ' + label_text)
    new_lines.append('\n')
    # if len(img_letters.letters) == len(label_letters.letters):
    #     flag = True
    #     for i in range(0, len(label_letters.letters)):
    #         flag = flag and (img_letters.letters[i].letter == label_letters.letters[i].letter)
    #     print(flag)
    # else:
    #     print(False)
    compare_result = compare(result_text,label_text)
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
