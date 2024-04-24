import os

dir1 = 'dataset/val/labels'
dir2 = 'dataset_b/val/labels'
files1 = os.listdir(dir1)
files2 = os.listdir(dir2)
print(sorted(files1) == sorted(files2))
