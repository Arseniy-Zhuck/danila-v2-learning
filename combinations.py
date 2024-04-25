from itertools import combinations
n = 10
lst = [i for i in range(0,n)]
array = ['a','b','c','d','e','f','g','h','i','j']
for i in range(1,n-1):
    for comb in combinations(lst, i):
        comb_list = list(comb)
        print(comb)
