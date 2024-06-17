from data_classes.letters_in_image import Letters_In_Image, Yolo_label_Rect, Letter_In_Image

import json

import torch
import cv2
import os

from word_compare_result import Word_compare_result

# model and dataset
model_path = 'models/vagon_number_recognize/06_16_9000_im/exp41/weights/text_recognize_yolo.pt'
dir_path = 'vagon_number_recognize/dataset_test/'
label_path = dir_path + 'numbers.txt'
image_dir_path = dir_path + 'numbers'
test_result = 'vagon_number_recognize/06_16_9000_im'
str1 = 'models/vagon_number_recognize/06_16_9000_im/exp41/weights/text_recognize_yolo.pt\n'


# useful addresses
yolo_path = 'yolov5'
image_dir = os.listdir(image_dir_path)
model = torch.hub.load(yolo_path, 'custom', model_path, source='local')


data = {}
with open(label_path) as f:
    for line in f:
        lst = line.split()
        data[lst[0]] = lst[1]


print(str1)
sizes_h = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
sizes_w = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384]
new_new_lines = []
for size_h in sizes_h:
    for size_w in sizes_w:
        counts = {Word_compare_result.equal: 0, Word_compare_result.partial: 0, Word_compare_result.none: 0,
                  Word_compare_result.wrong: 0}
        per_cents = {Word_compare_result.equal: 0.0, Word_compare_result.partial: 0.0, Word_compare_result.none: 0.0,
                     Word_compare_result.wrong: 0.0}
        new_lines = []
        new_lines.append(str1 + '\n')

        test_results = test_result + '_' + str(size_h) + '_' + str(size_w) + '.txt'
        new_lines.append(test_results)
        new_new_lines.append(test_results)
        new_new_lines.append('\n')
        print(test_results)
        for image_name in image_dir:
            img_path = image_dir_path + '/' + image_name
            img = cv2.imread(img_path)
            h, w = img.shape[:2]
            # model.max_det = 8
            results = model([img_path], size = (size_h,size_w))
            json_res = results.pandas().xyxy[0].to_json(orient="records")
            res2 = json.loads(json_res)
            img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
            letters_copy = img_letters.letters.copy()
            img_letters.sort_letters()
            img_letters.delete_intersections()
            img_letters.delete_x_intersections()
            if len(img_letters.letters) > 8:
                img_letters.letters = img_letters.letters[0:8]
            # label_path = label_dir_path + '/' + image_name.split('.')[0] + '.txt'
            label_letters = Letters_In_Image()
            d = data[image_name]
            for letter in d:
                label_letters.letters.append(Letter_In_Image(letter))

            # if len(img_letters.letters) == len(label_letters.letters):
            #     flag = True
            #     for i in range(0, len(label_letters.letters)):
            #         flag = flag and (img_letters.letters[i].letter == label_letters.letters[i].letter)
            #     print(flag)
            # else:
            #     print(False)
            compare_result = Letters_In_Image.compare(img_letters, label_letters)
            counts[compare_result] += 1
            if compare_result != Word_compare_result.equal:
                img1 = img.copy()
                for let in img_letters.letters:
                    cv2.rectangle(img1, (let.rect.xmin, let.rect.ymin),
                                  (let.rect.xmax, let.rect.ymax), (0, 0, 255), 2)
                    os.makedirs(test_result + '_' + str(size_h) + '_' + str(size_w), exist_ok=True)
                    cv2.imwrite(test_result + '_' + str(size_h) + '_' + str(size_w) + '/res_' + image_name, img1)
                img2 = img.copy()
                for let in letters_copy:
                    cv2.rectangle(img2, (let.rect.xmin, let.rect.ymin),
                                  (let.rect.xmax, let.rect.ymax), (0, 0, 255), 2)
                    os.makedirs(test_result + '_' + str(size_h) + '_' + str(size_w), exist_ok=True)
                    cv2.imwrite(test_result + '_' + str(size_h) + '_' + str(size_w) + '/whole_letters_' + image_name, img2)
                new_lines.append(img_letters.make_word() + ' - ' + label_letters.make_word())
                new_lines.append('\n')
        print(counts)
        new_lines.append(str(counts))
        for (result,count) in counts.items():
            per_cents[result] = round(count / float(len(image_dir)), 3) * 100
        print(per_cents)
        new_lines.append('\n')
        new_lines.append(str(per_cents))
        new_new_lines.append(str(counts))
        new_new_lines.append('\n')
        new_new_lines.append(str(per_cents))
        new_new_lines.append('\n')
        with open(test_results, "w") as new_f:
            new_f.writelines(new_lines)
with open(test_result + '.txt', 'w') as new_new_f:
    new_new_f.writelines(new_new_lines)
