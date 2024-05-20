import json
import torch
yolo_path = 'yolov5'
model_path = 'models/letters-detect/26_04_1000/exp8/weights/best.pt'
img_path = 'letters-detect/dataset_n/test/images/0ae838e9-cut_165.jpg'

model = torch.hub.load(yolo_path, 'custom', model_path, source='local')
model.max_det = 1
results = model([img_path], size = 32)
json_res = results.pandas().xyxy[0].to_json(orient="records")
res2 = json.loads(json_res)

print(res2)

