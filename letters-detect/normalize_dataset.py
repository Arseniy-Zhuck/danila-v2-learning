import os
from itertools import combinations
class TwoCifr:
    def __init__(self, file_name, lines):
        self.file_name = file_name
        cifrs = []
        for line in lines:
            cifr = line.split(' ')[0]
            cifrs.append(cifr)
        self.cifrs = cifrs


    def has_cifr(self, cifr):
        return cifr in self.cifrs

    def count_cifr(self, cifr):
        self.cifrs.count(cifr)

class CifrCount:
    def __init__(self):
        self.letters_counts = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

    def whole_count(self):
        return sum(self.letters_counts.values())

    def inc_cifr_count(self, letter):
        self.letters_counts[letter] += 1

    def up_cifr_counts(self, two_cifr):
        for cifr in two_cifr.cifrs:
            self.inc_cifr_count(cifr)

    def min_cifr_count(self):
        return min(self.letters_counts.values())

    def cif_count_difference(self):
        return max(self.letters_counts.values()) - min(self.letters_counts.values())

class TwoCifrArray:
    def __init__(self):
        self.two_cif_array = []


    def build_two_cifr_subset(self, list):
        subset_two_cifr_array = TwoCifrArray()
        for ind in list:
            subset_two_cifr_array.add_two_cifr(self.two_cif_array[ind])
        return subset_two_cifr_array

    def length(self):
        return len(self.two_cif_array)

    def add_two_cifr(self, two_cifr):
        self.two_cif_array.append(two_cifr)

    def count_cifrs(self):
        cifr_count = CifrCount()
        for two_cifr in self.two_cif_array:
            cifr_count.up_cifr_counts(two_cifr)
        return cifr_count

dataset_dir = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img\labels'
files = os.listdir(dataset_dir)
main_array = TwoCifrArray()
for file in files:
    whole_file_name = dataset_dir + '\\' + file
    file_name = file.split('.')[0]
    with open(whole_file_name, "r") as f:
        lines = []
        for line in f:
            lines.append(line)
        main_array.add_two_cifr(TwoCifr(file_name, lines))
initial_cifr_count = main_array.count_cifrs()
MIN_CIFR_COUNT = initial_cifr_count.min_cifr_count()
min_difference = initial_cifr_count.cif_count_difference()
best_subset = main_array
n = main_array.length()
lst = [i for i in range(0,n)]
j = 0
for i in range(MIN_CIFR_COUNT * 5, (MIN_CIFR_COUNT + 20) * 5):
    for comb in combinations(lst, i):
        comb_list = list(comb)
        subset_two_cifr_array = main_array.build_two_cifr_subset(comb_list)
        subset_cifr_count = subset_two_cifr_array.count_cifrs()
        min_cifr_count_s = subset_cifr_count.min_cifr_count()
        difference = subset_cifr_count.cif_count_difference()
        if ((j % 100000) == 0):
            print(subset_cifr_count.letters_counts)
            print(str(j) + ' combinations checked + i = ' + str(i))
            print(':  ' + str(min_cifr_count_s) + ' ' + str(difference) + ' imgscount = ' + str(subset_cifr_count.whole_count()))
        if (min_cifr_count_s == MIN_CIFR_COUNT) & (difference < min_difference):
            best_subset = subset_two_cifr_array
            min_difference = difference
            print('ALARM!!!! CHANGE!!!!!')
        j += 1
new_lines = []
for two_cifr in best_subset.two_cif_array:
    new_lines.append(two_cifr.file_name)
with open('C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\files.txt', "w") as new_f:
    new_f.writelines(new_lines)
print("URA___KOPIROVANIEFAILOV")
old_addr_imgs = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img\images\\'
old_addr_labels = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img\labels\\'
new_addr_imgs = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\\normalized_dataset\images\\'
new_addr_labels = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\\normalized_dataset\labels\\'
import shutil

for file_name in new_lines:
    old_img_name = old_addr_imgs + file_name + '.jpg'
    old_label_name = old_addr_labels + file_name + '.txt'
    new_img_name = new_addr_imgs + file_name + '.jpg'
    new_label_name = new_addr_labels + file_name + '.txt'
    shutil.copy2(old_label_name, new_label_name)
    shutil.copy2(old_img_name, new_img_name)