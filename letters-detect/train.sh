python train.py --img 32 --batch 4 --epochs 40 --data 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\dataset.yaml' --weights 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\yolov5x.pt' --nosave --cache
python detect.py --source 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\dataset\test\images' --weights 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\models\letters-detect\24_04\last.pt' --save-txt --save-crop --imgsz 32 --max-det 2
python detect.py --source 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\dataset\train\images' --weights 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\models\letters-detect\24_04\last.pt' --save-txt --save-crop --imgsz 32 --max-det 2
python train.py --img 32 --batch 4 --epochs 40 --data 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\dataset.yaml' --weights 'C:\Users\a_zhuck\Documents\GitHub\danila-v2-learning\models\letters-detect\24_04\last.pt' --nosave --cache