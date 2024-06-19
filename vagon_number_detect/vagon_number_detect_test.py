import os
import torch
import json
import cv2
import sys

def IOU(xmin, xmax, ymin, ymax, xmin_t, xmax_t, ymin_t, ymax_t,h,w):
    I = 0
    U = 0
    for i in range(0, w):
        for j in range(0, h):
            flag = ((i <= xmax) and (i >= xmin) and (j <= ymax) and (j >= ymin))
            flag_t = ((i <= xmax_t) and (i >= xmin_t) and (j <= ymax_t) and (j >= ymin_t))
            if (flag and flag_t):
                I += 1
            if (flag or flag_t):
                U += 1
    resultat = I / float(U)
    return resultat

def test_yollov5(dir, labels_dir, flag):
    ds = ''
    if (flag):
        ds = ds + 'Learning-dataset: '
    else:
        ds = ds + 'Testing-dataset: '
    print(ds + 'starts')
    model = torch.hub.load(yolo_path, 'custom', path=model_path, source='local')
    n = 0
    files = os.listdir(dir)
    sum_IOU = 0
    correct_answers70 = 0
    correct_answers80 = 0
    correct_answers90 = 0
    for file in files:

        if (n % 50)==1:
            per_cent70 = correct_answers70 / float(n)
            per_cent80 = correct_answers80 / float(n)
            per_cent90 = correct_answers90 / float(n)
            av_IOU = sum_IOU / float(n)
            print(str(n) + ' tests - 70_IOU ' + str(round(per_cent70, 4)) + ', 80_IOU ' + str(round(per_cent80, 4)) +
                  ', 90_IOU ' + str(round(per_cent90, 4))  + ', av_IOU = ' + str(round(av_IOU,4)))
        whole_file_name = dir + '\\' + file
        img = cv2.imread(whole_file_name)
        results = model([whole_file_name])
        json_res = results.pandas().xyxy[0].to_json(orient="records")
        res2 = json.loads(json_res)
        if len(res2) > 0:
            index_of_max_S = 0
            S = 0
            for index in range(len(res2)):
                xmin_cur = int(float(res2[index]['xmin']))
                xmax_cur = int(float(res2[index]['xmax']))
                ymin_cur = int(float(res2[index]['ymin']))
                ymax_cur = int(float(res2[index]['ymax']))
                h_cur = ymax_cur - ymin_cur
                w_cur = xmax_cur - xmin_cur
                S_cur = h_cur * w_cur
                if S_cur > S:
                    index_of_max_S = index
                    S = S_cur
            xmin = int(float(res2[index_of_max_S]['xmin']))
            xmax = int(float(res2[index_of_max_S]['xmax']))
            ymin = int(float(res2[index_of_max_S]['ymin']))
            ymax = int(float(res2[index_of_max_S]['ymax']))

            data = []
            whole_label_name = labels_dir + '\\' + file.split('.')[0] + '.txt'
            with open(whole_label_name) as f:
                for line in f:
                    data.append([float(x) for x in line.split()])
            h, w = img.shape[:2]
            l_index_of_max_S = 0
            l_S = 0
            for l_index in range(len(data)):
                l_xmin_cur = int((data[l_index][1] - data[l_index][3] / 2) * w)
                l_xmax_cur = int((data[l_index][1] + data[l_index][3] / 2) * w)
                l_ymin_cur = int((data[l_index][2] - data[l_index][4] / 2) * h)
                l_ymax_cur = int((data[l_index][2] + data[l_index][4] / 2) * h)
                l_h_cur = l_ymax_cur - l_ymin_cur
                l_w_cur = l_xmax_cur - l_xmin_cur
                l_S_cur = l_h_cur * l_w_cur
                if l_S_cur > l_S:
                    l_index_of_max_S = l_index
                    l_S = l_S_cur
            xmin_t = int((data[l_index_of_max_S][1] - data[l_index_of_max_S][3] / 2) * w)
            xmax_t = int((data[l_index_of_max_S][1] + data[l_index_of_max_S][3] / 2) * w)
            ymin_t = int((data[l_index_of_max_S][2] - data[l_index_of_max_S][4] / 2) * h)
            ymax_t = int((data[l_index_of_max_S][2] + data[l_index_of_max_S][4] / 2) * h)
            IOU_value = IOU(xmin, xmax, ymin, ymax, xmin_t, xmax_t, ymin_t, ymax_t, h= h, w= w)
        else:
            IOU_value = 0.0
        if IOU_value > 0.7:
            correct_answers70+=1
        if IOU_value > 0.8:
            correct_answers80+=1
        if IOU_value > 0.9:
            correct_answers90+=1
        n+=1
        sum_IOU += IOU_value
        # print(file, IOU_value)
    per_cent70 = correct_answers70 / float(n)
    per_cent80 = correct_answers80 / float(n)
    per_cent90 = correct_answers90 / float(n)
    av_IOU = sum_IOU / float(n)
    print(ds + str(n) + ' tests - 70_IOU ' + str(round(per_cent70, 4)) + ', 80_IOU ' + str(round(per_cent80, 4)) +
                  ', 90_IOU ' + str(round(per_cent90, 4))  + ', av_IOU = ' + str(round(av_IOU,4)))

model_path = 'models/vagon_number_detect/19_06_03/exp42/weights/last.pt'
yolo_path = 'yolov5'
dir = 'vagon_number_detect/dataset/test/images'
labels_dir = 'vagon_number_detect/dataset/test/labels'
test_yollov5(dir, labels_dir, False)

# if (len(sys.argv) == 1):
#     print('Please enter file with weights')
# else:
#     # img = cv2.imread('C:\\Users\\a_zhuck\PycharmProjects\dl-rama-no-spring-detect\\3cf59068-338.jpeg')
#
#     if (sys.argv[2]=='train'):
#         dir = 'vagon_number_detect/dataset/train/images'
#         labels_dir = 'vagon_number_detect/dataset/train/labels'
#         test_yollov5(dir, labels_dir, True)
#     else:
#         dir = 'vagon_number_detect/dataset/test/images'
#         labels_dir = 'vagon_number_detect/dataset/test/labels'
#         test_yollov5(dir, labels_dir, False)
