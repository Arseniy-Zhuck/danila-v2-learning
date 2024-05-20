import os
import shutil
dir = 'letters-detect/ruzhimmash/dataset_7500_b_7500_r'
ss = ['val', 'test', 'train']
tt = ['images','labels']


for s in ss:
    for t in tt:
        whole_dir = dir + '/' + s + '/' + t
        work_dir = os.listdir(whole_dir)
        for file_name in work_dir:
            work_file_path = whole_dir + '/' + file_name
            shutil.copy(work_file_path, whole_dir + '/' + file_name.split('.')[0] + '2' + '.' + file_name.split('.')[1])
            shutil.copy(work_file_path, whole_dir + '/' + file_name.split('.')[0] + '3' + '.' + file_name.split('.')[1])
            shutil.copy(work_file_path, whole_dir + '/' + file_name.split('.')[0] + '4' + '.' + file_name.split('.')[1])
            shutil.copy(work_file_path, whole_dir + '/' + file_name.split('.')[0] + '5' + '.' + file_name.split('.')[1])
