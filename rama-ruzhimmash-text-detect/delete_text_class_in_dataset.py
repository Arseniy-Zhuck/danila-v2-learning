import os

dir = 'rama-ruzhimmash-text-detect/dataset/val/labels'
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
        if numbers[0] != '2':
            new_line = ' '.join(numbers)
            new_lines.append(new_line)
    new_file_name = 'rama-ruzhimmash-text-detect/dataset_no_text/val/labels' + '\\' + file
    with open(new_file_name, "w") as new_f:
        new_f.writelines(new_lines)
