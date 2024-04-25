import os
dataset_dir = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img\labels'
files = os.listdir(dataset_dir)
letters_counts = {'0':0, '1':0, '2':0,'3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0}
for file in files:
    whole_file_name = dataset_dir + '\\' + file
    with open(whole_file_name, "r") as f:
        lines = []
        for line in f:
            lines.append(line)
        for line in lines:
            numbers = line.split(' ')
            letters_counts[numbers[0]] +=1
print(letters_counts)