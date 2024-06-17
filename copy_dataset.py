import os
import shutil
dir = 'vagon_number_recognize/dataset_9000'
ss = ['val', 'test', 'train']
tt = ['images','labels']


for s in ss:
    for t in tt:
        whole_dir = dir + '/' + s + '/' + t
        work_dir = os.listdir(whole_dir)
        for file_name in work_dir:
            work_file_path = whole_dir + '/' + file_name
            shutil.copy(work_file_path, whole_dir + '/' + '2' + file_name[:file_name.rfind('.')] + '2' + '.' + file_name[(file_name.rfind('.')+1):])
            shutil.copy(work_file_path, whole_dir + '/' + '3' + file_name[:file_name.rfind('.')] + '3' + '.' + file_name[(file_name.rfind('.')+1):])
            shutil.copy(work_file_path, whole_dir + '/' + '4' + file_name[:file_name.rfind('.')] + '4' + '.' + file_name[(file_name.rfind('.')+1):])
            shutil.copy(work_file_path, whole_dir + '/' + '5' + file_name[:file_name.rfind('.')] + '5' + '.' + file_name[(file_name.rfind('.')+1):])
