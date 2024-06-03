import json
from data_classes.letters_in_image import Letters_In_Image, Yolo_label_Rect, Letter_In_Image

import cv2
import torch
yolo_path = 'yolov5'
model_path = 'models/letters-detect/21_05_30_11000_b_11000_r/exp37/weights/last.pt'
img_path = 'letters-detect/0b0a19fb-59445031.jpg'

model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
# model.max_det = 1
results = model([img_path], size = (32,256))
json_res = results.pandas().xyxy[0].to_json(orient="records")
res2 = json.loads(json_res)
img_letters = Letters_In_Image.get_letters_in_image_from_yolo_json(res2)
img_letters.sort_letters()
img_letters.delete_intersections()
print(img_letters)
print(img_letters.make_word())
img = cv2.imread(img_path)
for bound in img_letters.letters:
    cv2.rectangle(img,(bound.rect.xmin,bound.rect.ymin),(bound.rect.xmax,bound.rect.ymax), (0, 0, 255), 2)
    cv2.putText(img, bound.letter, (bound.rect.xmin,bound.rect.ymin), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 255), 2)
# print(res2)
cv2.namedWindow('vagon', cv2.WINDOW_AUTOSIZE)
cv2.imshow('vagon', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

