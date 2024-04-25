import os
dataset_dir = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img1\labels'
files = os.listdir(dataset_dir)
letters_counts = {'0':0, '1':0, '2':0,'3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
for file in files:
    whole_file_name = dataset_dir + '\\' + file
    with open(whole_file_name, "r") as f:
        lines = []
        for line in f:
            lines.append(line)
    if len(lines)==2:
        three = lines[0].split(' ')[0]
        one = lines[1].split(' ')[0]
        if (three == '3') and (one == '1'):
            os.remove(whole_file_name)
            img_name = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img1\images' + '\\' + file.split('.')[0] + '.jpg'
            os.remove(img_name)
