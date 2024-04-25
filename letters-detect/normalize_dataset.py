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

    def min_cifr(self):
        cifr_m = '0'
        min_cifr = self.letters_counts['0']
        for cifr in self.letters_counts.keys():
            if self.letters_counts[cifr] < min_cifr:
                min_cifr = self.letters_counts[cifr]
                cifr_m = cifr
        return cifr_m, min_cifr

    def cif_count_difference(self):
        return max(self.letters_counts.values()) - min(self.letters_counts.values())

class TwoCifrArray:

    @staticmethod
    def union(list1, list2):
        new_list =  list1.two_cif_array + list2.two_cif_array
        new_obj = TwoCifrArray()
        new_obj.two_cif_array = new_list
        return new_obj

    def __init__(self):
        self.two_cif_array = []

    def build_min_array(self):
        subset_min = TwoCifrArray()
        least_subset = TwoCifrArray()
        cifr_count = self.count_cifrs()
        min_count_cifr, min_count = cifr_count.min_cifr()
        for two_cifr in self.two_cif_array:
            if two_cifr.has_cifr(min_count_cifr):
                subset_min.add_two_cifr(two_cifr)
            else:
                least_subset.add_two_cifr(two_cifr)
        return subset_min, least_subset

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

dataset_dir = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img1\labels'
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
subset_min, least_subset = main_array.build_min_array()
print(initial_cifr_count.letters_counts)
print(':  ' + str(MIN_CIFR_COUNT) + ' ' + str(min_difference) + ' imgscount = ' + str(initial_cifr_count.whole_count()))

m = least_subset.length()
lst = [i for i in range(0,m)]
j = 0
for i in range(MIN_CIFR_COUNT * 4 + 2, (MIN_CIFR_COUNT) * 4 + 3):
    for comb in combinations(lst, i):
        comb_list = list(comb)
        subset_without_min = least_subset.build_two_cifr_subset(comb_list)
        subset_two_cifr_array = TwoCifrArray.union(subset_min,subset_without_min)
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
            new_lines = []
            for two_cifr in best_subset.two_cif_array:
                new_lines.append(two_cifr.file_name)
            with open('C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\\files.txt', "w") as new_f:
                new_f.writelines(new_lines)
            print("URA___KOPIROVANIEFAILOV")
            old_addr_imgs = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img1\images\\'
            old_addr_labels = 'C:\\Users\\a_zhuck\Documents\GitHub\danila-v2-learning\letters-detect\labeled_img1\labels\\'
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
        j += 1
