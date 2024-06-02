import json
import os

import cv2
import torch
from word_compare_result import Word_compare_result
from enum import Enum
from enum import Enum

class Text_label_IOU_results:
    def __init__(self):
        self.sum = 0.0
        self.avg = 0.0
        self.count = 0

    def add(self, IoU):
        self.sum += IoU
        self.count += 1
        self.avg = round(self.sum / self.count, 3) * 100

    def to_str(self):
        return str(self.avg)

class Text_label_IOU_count_results:
    def __init__(self, per_cent_border):
        self.per_cent_border = per_cent_border
        self.sum = 0
        self.avg = 0.0
        self.count = 0

    def inc(self, IoU):
        if IoU > self.per_cent_border:
            self.sum += 1
        self.count += 1
        self.avg = round(self.sum / float(self.count), 3) * 100

    def to_str(self):
        return str(round(self.per_cent_border, 3) * 100) + ' count = ' + str(self.sum) + ', per_cent = ' + str(self.avg)

class Text_class_results:
    def __init__(self, class_text, low, middle, high):
        self.class_text = class_text
        self.counts = {Text_results.none:0,Text_results.exists:0,Text_results.few:0,Text_results.whole:0}
        self.per_cents = {Text_results.none: 0.0, Text_results.exists: 0.0, Text_results.few: 0.0, Text_results.whole: 100.0}
        self.IoU_exists = Text_label_IOU_results()
        self.IoU = Text_label_IOU_results()
        self.list_text_label_IOU_count_results = [Text_label_IOU_count_results(low), Text_label_IOU_count_results(middle), Text_label_IOU_count_results(high)]

    def add_result(self, text_result_test):
        self.counts[text_result_test.found] += 1
        self.counts[Text_results.whole] += 1
        self.per_cents[text_result_test.found] = round(self.counts[text_result_test.found] / float(self.counts[Text_results.whole]), 3) * 100
        self.IoU.add(text_result_test.IoU)
        if text_result_test.found == Text_results.exists:
            self.IoU_exists.add(text_result_test.IoU)
        for text_label_IOU_count_result in self.list_text_label_IOU_count_results:
            text_label_IOU_count_result.inc(text_result_test.IoU)

    def to_str(self):
        res = ''
        for text_results in self.counts.keys():
            res += text_results.name
            res += ' : '
            res += str(self.counts[text_results])
            res += ', '
        res += '\n'
        for text_results in self.per_cents.keys():
            res += text_results.name
            res += ' : '
            res += str(self.per_cents[text_results])
            res += ', '
        res += '\n'
        res += 'avg_IoU : ' + self.IoU.to_str() + '\n'
        res += 'avg_IoU_exists : ' + self.IoU_exists.to_str() + '\n'
        for text_label_IOU_count_result in self.list_text_label_IOU_count_results:
            res += text_label_IOU_count_result.to_str()
        res += '\n'
        return res

class Image_results:
    def __init__(self, low, middle, high):
        self.dict = {
            Class_text.number : Text_class_results(Class_text.number, low, middle, high),
            Class_text.prod: Text_class_results(Class_text.prod, low, middle, high),
            Class_text.year: Text_class_results(Class_text.year, low, middle, high)
        }

    def add_result(self, test_result):
        for class_text in self.dict.keys():
            self.dict[class_text].add_result(test_result[class_text])

    def to_str(self):
        res = ''
        for class_text in self.dict.keys():
            res += class_text.name + '\n'
            res += self.dict[class_text].to_str()
            res += '\n'
        return res

class Text_results(Enum):
    none = 0
    exists = 1
    few = 2
    whole = 3

class Text_result_test:
    def __init__(self, found, IoU):
        self.found = found
        self.IoU = IoU

    def __str__(self):
        return self.found.name + ', IoU : ' + str(round(self.IoU, 3) * 100) + '%'

class Class_text(Enum):
    number = 0
    prod = 1
    text = 2
    year = 3

class Rect:
    # прочитать из json результата йоло

    @staticmethod
    def find_max_IoU(rect_list1, rect_list2):
        max_IoU = 0.0
        for rect1 in rect_list1:
            for rect2 in rect_list2:
                cur_IoU = rect1.IoU(rect2)
                if cur_IoU > max_IoU:
                    max_IoU = cur_IoU
        return max_IoU

    @staticmethod
    def get_rect_from_yolo_json(yolo_json):
        xmin = int(float(yolo_json['xmin']))
        xmax = int(float(yolo_json['xmax']))
        ymin = int(float(yolo_json['ymin']))
        ymax = int(float(yolo_json['ymax']))
        rect = Rect(xmin, xmax, ymin, ymax)
        return rect

    def __init__(self, xmin=0, xmax=0, ymin=0, ymax=0):
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    # Найти IOU между этим прямоугольником и другим, данным в объекте
    def IoU(self, rect):
        def IOU(xmin, xmax, ymin, ymax, xmin_t, xmax_t, ymin_t, ymax_t):
            I = 0
            U = 0
            xmin_U = min(xmin, xmin_t)
            xmax_U = max(xmax, xmax_t)
            ymin_U = min(ymin, ymin_t)
            ymax_U = max(ymax, ymax_t)
            h = ymax_U - ymin_U
            w = xmax_U - xmin_U
            for i in range(xmin_U, xmax_U):
                for j in range(ymin_U, ymax_U):
                    flag = ((i <= xmax) and (i >= xmin) and (j <= ymax) and (j >= ymin))
                    flag_t = ((i <= xmax_t) and (i >= xmin_t) and (j <= ymax_t) and (j >= ymin_t))
                    if (flag and flag_t):
                        I += 1
                    if (flag or flag_t):
                        U += 1
            resultat = I / float(U)
            return resultat
        return IOU(self.xmin, self.xmax, self.ymin, self.ymax,
                   rect.xmin, rect.xmax, rect.ymin, rect.ymax)

    def __str__(self):
        res = ('xmin = ' + str(self.xmin) + ', xmax = ' + str(self.xmax) + ', ymin = ' + str(self.ymin) +
               ', ymax = ' + str(self.ymax))
        return res

    def intersection(self, rect):
        h = max(self.ymax, rect.ymax) - min(self.ymin, rect.ymin)
        w = max(self.xmax, rect.xmax) - min(self.xmin, rect.xmin)
        I = 0
        U = 0
        for i in range(0, w):
            for j in range(0, h):
                flag = ((i <= self.xmax) and (i >= self.xmin) and (j <= self.ymax) and (j >= self.ymin))
                flag_t = ((i <= rect.xmax) and (i >= rect.xmin) and (j <= rect.ymax) and (j >= rect.ymin))
                if (flag and flag_t):
                    I += 1
        return I

    def union(self, rect):
        new_xmin = min(self.xmin, rect.xmin)
        new_ymin = min(self.ymin, rect.ymin)
        new_xmax = max(self.xmax, rect.xmax)
        new_ymax = max(self.ymax, rect.ymax)
        return Rect(new_xmin, new_xmax, new_ymin, new_ymax)

class Yolo_label_Rect:

    @staticmethod
    def build_from_2D_array(data, h, w):
        return Yolo_label_Rect(data[1], data[3], data[2], data[4], h, w)

    def __init__(self, xc=0.0, ow=0.0, yc=0.0, oh=0.0, h=0.0, w=0.0):
        self.xc = xc
        self.ow = ow
        self.yc = yc
        self.oh = oh
        self.w = w
        self.h = h


    def build_rect(self):
        xmin_t = int((self.xc - self.ow / 2) * self.w)
        xmax_t = int((self.xc + self.ow / 2) * self.w)
        ymin_t = int((self.yc - self.oh / 2) * self.h)
        ymax_t = int((self.yc + self.oh / 2) * self.h)
        return Rect(xmin_t, xmax_t, ymin_t, ymax_t)


class Text_In_Image:
    def __init__(self, obj, rect = None, confidence=0.0):
        self.obj = obj
        self.rect = rect
        self.confidence = float(confidence)

    @staticmethod
    def make_rect_array(texts_in_image):
        rects = []
        for text_in_image in texts_in_image:
            rects.append(text_in_image.rect)
        return rects

    @staticmethod
    def get_obj_in_image_from_yolo_json(letter_json):
        return Text_In_Image(Class_text(int(letter_json['class'])), Rect.get_rect_from_yolo_json(letter_json), letter_json['confidence'])

    def __eq__(self, other):
        return (other is Text_In_Image) & (self.obj == other.obj)

    def __hash__(self):
        return hash(self.obj)

    def __str__(self):
        res_dict = {'obj' : self.obj.name, 'xmin' : self.rect.xmin, 'xmax' : self.rect.xmax, 'ymin' : self.rect.ymin, 'ymax' : self.rect.ymax, 'confidence' : self.confidence}
        return str(res_dict)

class Objs_In_Image:
    def __init__(self):
        self.objs = []
        self.dict = {Class_text.number:[],Class_text.prod:[],Class_text.text:[],Class_text.year:[]}

    @staticmethod
    def get_objs_in_image_from_yolo_json(objs_json):
        objs_in_image = Objs_In_Image()
        for obj_json in objs_json:
            objs_in_image.objs.append(Text_In_Image.get_obj_in_image_from_yolo_json(obj_json))
        return objs_in_image

    def delete_intersections(self):
        new_objs = []
        i = 0
        while i < len(self.objs) - 1:
            IoU = self.objs[i].rect.IoU(self.objs[i+1].rect)
            if IoU > 0.5:
                new_obj = self.objs[i] if self.objs[i].confidence > self.objs[i + 1].confidence else self.objs[i + 1]
                i += 2
            else:
                new_obj = self.objs[i]
                i += 1
            new_objs.append(new_obj)
        if (i == len(self.objs) - 1):
            new_objs.append(self.objs[i])
        self.objs = new_objs

    def __str__(self):
        res = ''
        for text_class in self.dict.keys():
            res = res + text_class.name +'\n'
            for obj_in_image in self.dict[text_class]:
                res = res + obj_in_image.__str__() + '\n'
        return res

    def make_dict(self):
        for obj in self.objs:
            self.dict[obj.obj].append(obj)

    @staticmethod
    def compare_images(image_objs, label_objs):
        v1 = Text_result_test(Text_results.none, 0.0)
        v2 = Text_result_test(Text_results.none, 0.0)
        v3 = Text_result_test(Text_results.none, 0.0)
        results = {
                    Class_text.number: v1,
                    Class_text.prod: v2,
                    Class_text.year: v3
        }
        if len(image_objs.dict[Class_text.year]) == 0:
            results[Class_text.year].found = Text_results.none
        else:
            if len(label_objs.dict[Class_text.year])==1:
                if len(image_objs.dict[Class_text.year]) == 1:
                    results[Class_text.year].found = Text_results.exists
                    results[Class_text.year].IoU = image_objs.dict[Class_text.year][0].rect.IoU(label_objs.dict[Class_text.year][0].rect)
                else:
                    results[Class_text.year].found = Text_results.few
            else:
                results[Class_text.year].found = Text_results.exists
                results[Class_text.year].IoU = Rect.find_max_IoU(
                    Text_In_Image.make_rect_array(image_objs.dict[Class_text.year]),
                    Text_In_Image.make_rect_array(label_objs.dict[Class_text.year])
                                                  )
        if len(image_objs.dict[Class_text.prod]) == 0:
            results[Class_text.prod].found = Text_results.none
        else:
            if len(label_objs.dict[Class_text.prod])==1:
                if len(image_objs.dict[Class_text.prod]) == 1:
                    results[Class_text.prod].found = Text_results.exists
                    results[Class_text.prod].IoU = image_objs.dict[Class_text.prod][0].rect.IoU(label_objs.dict[Class_text.prod][0].rect)
                else:
                    results[Class_text.prod].found = Text_results.few
            else:
                results[Class_text.prod].found = Text_results.exists
                results[Class_text.prod].IoU = Rect.find_max_IoU(
                    Text_In_Image.make_rect_array(image_objs.dict[Class_text.prod]),
                    Text_In_Image.make_rect_array(label_objs.dict[Class_text.prod])
                )
        if len(image_objs.dict[Class_text.number]) == 0:
            results[Class_text.number].found = Text_results.none
        else:
            if len(label_objs.dict[Class_text.number]) == 1:
                if len(image_objs.dict[Class_text.number]) == 1:
                    results[Class_text.number].found = Text_results.exists
                    results[Class_text.number].IoU = image_objs.dict[Class_text.number][0].rect.IoU(
                        label_objs.dict[Class_text.number][0].rect)
                else:
                    results[Class_text.number].found = Text_results.few
            else:
                results[Class_text.number].found = Text_results.exists
                results[Class_text.number].IoU = Rect.find_max_IoU(
                    Text_In_Image.make_rect_array(image_objs.dict[Class_text.number]),
                    Text_In_Image.make_rect_array(label_objs.dict[Class_text.number])
                )
        return results
# img_path = 'prod-classify-v1/dataset/test/images/0b62db71-126.jpg'
# label_path = 'prod-classify-v1/dataset/test/labels/0b62db71-126.txt'
def res_str(test_res):
    res_number = 'number : ' + str(test_res[Class_text.number]) + ';\n '
    res_prod = 'prod : ' + str(test_res[Class_text.prod]) + ';\n '
    res_year = 'year : ' + str(test_res[Class_text.year]) + ';\n '
    return res_number + res_prod + res_year


prod_name = 'ruzhimmash'
v = 6
d_s = 'test'
count = 1200
model_name = '2024y_6000im'
yolo_path = 'yolov5'
model_path = 'models/rama-text-' + prod_name + '-detect/' + model_name + '.pt'
dir_path = 'rama-' + prod_name + '-text-detect/dataset_1000/' + d_s
test_results = 'rama-' + prod_name + '-text-detect/test_results/v' + str(v) + '_' + model_name + '_' + d_s + '_' + str(count) + '.txt'
str1 = prod_name + '_v' + str(v) + '_' + model_name + '_' + d_s + '_' + str(count) + '\n'

# useful addresses
label_dir_path = dir_path + '/' + 'labels'
image_dir_path = dir_path + '/' + 'images'
yolo_path = 'yolov5'
image_dir = os.listdir(image_dir_path)
new_lines = []
model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
new_lines.append(str1)
# counts = {Prod_classify_result.wrong:0,Prod_classify_result.right:0,Prod_classify_result.two_prods:0,Prod_classify_result.no_prod:0}
# per_cents = {Prod_classify_result.wrong:0.0,Prod_classify_result.right:0.0,Prod_classify_result.two_prods:0.0,Prod_classify_result.no_prod:0.0}
image_results = Image_results(0.7,0.8,0.9)
n = 0
for image_name in image_dir:
    n += 1
    img_path = image_dir_path + '/' + image_name
    results = model([img_path], size = 256)
    json_res = results.pandas().xyxy[0].to_json(orient="records")
    res2 = json.loads(json_res)
    img_objs = Objs_In_Image.get_objs_in_image_from_yolo_json(res2)
    img_objs.delete_intersections()
    img_objs.make_dict()
    label_path = label_dir_path + '/' + image_name[:image_name.rfind('.')] + '.txt'
    data = []
    with open(label_path) as f:
        for line in f:
            data.append([float(x) for x in line.split()])
    img = cv2.imread(img_path)
    h, w = img.shape[:2]
    label_objs = Objs_In_Image()
    for d in data:
        yolo_label_rect = Yolo_label_Rect.build_from_2D_array(d, h, w)
        rect_labeled = yolo_label_rect.build_rect()
        label_objs.objs.append(Text_In_Image(Class_text(int(d[0])), rect_labeled))
    label_objs.make_dict()
    print(str(n) + '. ' + image_name)
    print(img_objs)
    print(label_objs)
    test_res = Objs_In_Image.compare_images(image_objs=img_objs,label_objs=label_objs)
    print(res_str(test_res))
    new_lines.append(str(n) + '. ' + image_name)
    new_lines.append(str(img_objs) + '\n')
    new_lines.append(str(label_objs) + '\n')
    new_lines.append(res_str(test_res))
    image_results.add_result(test_res)
str2 = image_results.to_str()
print(str2)
new_lines.append(str2)
with open(test_results, "w") as new_f:
    new_f.writelines(new_lines)


