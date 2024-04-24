import os

dir = 'prod-classify-v1/dataset_r/test/labels'
files = os.listdir(dir)
for file in files:
    whole_file_name = dir + '\\' + file
    with open(whole_file_name, "r") as f:
        lines = []
        for line in f:
            lines.append(line)
    new_lines = []
    for line in lines:
        numbers = line.split(' ')
        if numbers[0] == '1':
            numbers[0] = '1'
        else:
            numbers[0] = '2'
        new_line = ' '.join(numbers)
        new_lines.append(new_line)
    new_file_name = 'prod-classify-v1/dataset/test/labels' + '\\' + file
    with open(new_file_name, "w") as new_f:
        new_f.writelines(new_lines)
