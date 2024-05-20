import os
ss = ['test', 'val', 'train']
for s in ss:
    dir = 'rama-begickaya-text-detect/dataset/' + s + '/labels'
    files = os.listdir(dir)
    for file in files:
        print(s)
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
        new_file_name = 'rama-begickaya-text-detect/dataset_no_text/' + s + '/labels' + '\\' + file
        with open(new_file_name, "w") as new_f:
            new_f.writelines(new_lines)
