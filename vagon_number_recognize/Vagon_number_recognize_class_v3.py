import hashlib
import os
from datetime import datetime

import cv2
import numpy as np
from PIL.Image import Image
from easyocr import easyocr
import pytesseract


class Vagon_number_recognize_class_v3:
    # def __init__(self):
    #     # self.reader = pytesseract.pytesseract.image_to_string(Image.open(filename))

    def recognize(self, file_path):
        img = cv2.imread(file_path)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blur = cv2.GaussianBlur(gray, (3,3), 0.7)
        # ret, thresh = cv2.threshold(blur, 150, 255, cv2.THRESH_BINARY)
        # img_erode = cv2.erode(thresh, np.ones((3, 3), np.uint8), iterations=1)
        # counturs, hierarchy = cv2.findContours(img_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(img,counturs,-1, (0,0,0), 3, cv2.LINE_AA, hierarchy, 1 )
        # hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
        # hash_str = hash_object.hexdigest()
        # cut_vagon_img_prep = 'cut_vagon_img_prep' + hash_str + '.jpg'
        # cv2.imwrite(cut_vagon_img_prep, img)
        res = pytesseract.image_to_string(img)
        # os.remove(cut_vagon_img_prep)
        return res

    def work_image_cut(self, filepath):
        bounds = self.recognize(filepath)
        str_res = ''
        index = 0
        sum_conf = 0.0
        count_conf = 0
        avg_conf = 0.0
        if (len(bounds) > 0):
            for bound in bounds:
                if bound[2] > 0.5:
                    str_res += bound[1]
                    sum_conf += bound[2]
                    count_conf += 1
                    avg_conf = sum_conf / count_conf
        if len(str_res) > 8:
            len_str_res = len(str_res)
            min_index = 0
            min_conf = 1.1
            index = 0
            for bound in bounds:
                if (bound[2] < min_conf) and (bound[2] > 0.5):
                    min_index = index
                    min_conf = bound[2]
                index += 1
            if (len_str_res - len(bounds[min_index][1])) >= 8:
                str_res = ''
                index = 0
                sum_conf = 0.0
                count_conf = 0
                avg_conf = 0.0
                for bound in bounds:
                    if (bound[2] > 0.5) and index != min_index:
                        str_res += bound[1]
                        sum_conf += bound[2]
                        count_conf += 1
                        avg_conf = sum_conf / count_conf
                    index += 1
                return (str_res, avg_conf)
            else:
                str_res = ''
                index = 0
                sum_conf = 0.0
                count_conf = 0
                avg_conf = 0.0
                for bound in bounds:
                    if bound[2] > 0.5:
                        if (index != min_index):
                            str_res += bound[1]
                            sum_conf += bound[2]
                            count_conf += 1
                            avg_conf = sum_conf / count_conf
                        else:
                            new_length_without = 8 - (len_str_res - len(bounds[min_index][1]))
                            str_res += bound[1][0:new_length_without]
                            sum_conf += bound[2]
                            count_conf += 1
                            avg_conf = sum_conf / count_conf
                    index += 1
                return (str_res, avg_conf)
        else:
            return (str_res, avg_conf)

    def make_cuts(self, img_vagon, rect_array):
        number_image_cuts = []
        for rect in rect_array:
            number_image_cuts.append(img_vagon[rect.ymin:rect.ymax, rect.xmin:rect.xmax])
        return number_image_cuts

    def work_image(self, img_vagon, rect_array):
        image_text_areas = self.make_cuts(img_vagon, rect_array)
        numbers = []
        for image_text_area in image_text_areas:
            number = {'image_text_area' : image_text_area, 'text' : '', 's' : 0, 'conf' : 0.0}
            h, w = image_text_area.shape[:2]
            number['s'] = h * w
            hash_object = hashlib.md5(bytes(str(datetime.now()), 'utf-8'))
            hash_str = hash_object.hexdigest()
            img_cut_path = 'cut_text_img' + hash_str + '.jpg'
            cv2.imwrite(img_cut_path, image_text_area)
            (text, conf) = self.work_image_cut(img_cut_path)
            number['text'] = text
            number['conf'] = conf
            numbers.append(number)
            os.remove(img_cut_path)
        numbers.sort(key= lambda number : number['s'])
        if len(numbers) == 1:
            return (numbers[0]['text'], numbers[0]['conf'])
        else:
            if (len(numbers[0]['text']) != 8) and (len(numbers[1]['text']) == 8):
                return (numbers[1]['text'], numbers[1]['conf'])
            elif (len(numbers[0]['text']) == 8) and (len(numbers[1]['text']) != 8):
                return (numbers[0]['text'], numbers[0]['conf'])
            else:
                ans = sorted(numbers[0:2], key = lambda number : number['conf'])[0]
                return ans['text'], ans['conf']