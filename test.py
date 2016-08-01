# -*- coding: utf-8 -*-

def array_counts(data_array):
    counts = {}
    for i in data_array:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts

if __name__ == '__main__':
    a = ['a','g','a','g','ewew',123,33]
    print array_counts(a)
