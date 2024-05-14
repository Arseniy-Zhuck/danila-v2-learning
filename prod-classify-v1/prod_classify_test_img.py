import json
import cv2
import torch
from word_compare_result import Word_compare_result
from enum import Enum


class Rama_Prod(Enum):
    begickaya = 0
    ruzhimmash = 1
    text = 2

class Rect:
    # прочитать из json результата йоло

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


class Prod_In_Image:
    def __init__(self, obj, rect = None, confidence=0.0):
        self.obj = obj
        self.rect = rect
        self.confidence = float(confidence)


    @staticmethod
    def get_obj_in_image_from_yolo_json(letter_json):
        return Prod_In_Image(letter_json['name'], Rect.get_rect_from_yolo_json(letter_json), letter_json['confidence'])

    def __eq__(self, other):
        return (other is Prod_In_Image) & (self.obj == other.obj)

    def __hash__(self):
        return hash(self.obj)

    def __str__(self):
        res_dict = {'obj' : self.obj, 'xmin' : self.rect.xmin, 'xmax' : self.rect.xmax, 'ymin' : self.rect.ymin, 'ymax' : self.rect.ymax, 'confidence' : self.confidence}
        return str(res_dict)


class Objs_In_Image:
    def __init__(self):
        self.objs = []

    @staticmethod
    def get_objs_in_image_from_yolo_json(objs_json):
        objs_in_image = Objs_In_Image()
        for obj_json in objs_json:
            objs_in_image.objs.append(Prod_In_Image.get_obj_in_image_from_yolo_json(obj_json))
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
        for obj_in_image in self.objs:
            res = res + obj_in_image.__str__() + '\n'
        return res




img_path = 'prod-classify-v1/dataset/test/images/0b62db71-126.jpg'
label_path = 'prod-classify-v1/dataset/test/labels/0b62db71-126.txt'

yolo_path = 'yolov5'
model_path = 'models/prod-classify-v1/07_05_v1/exp/weights/last.pt'

model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
results = model([img_path], size = 256)
json_res = results.pandas().xyxy[0].to_json(orient="records")
res2 = json.loads(json_res)
img_objs = Objs_In_Image.get_objs_in_image_from_yolo_json(res2)
img_objs.delete_intersections()
# label_path = label_dir_path + '/' + image_name.split('.')[0] + '.txt'
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
    label_objs.objs.append(Prod_In_Image(Rama_Prod(int(d[0])).name, rect_labeled))
print(img_objs)
print(label_objs)


