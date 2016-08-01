# -*- coding: utf-8 -*-

def drop_mark(data_array):
    mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt',\
            'wd','wf','wn','wm','ws','wp','wb','wh',"tyc"]
    new_data_array = []
    for i in range(len(data_array)):
        temp_array = data_array[i].split()
        if len(temp_array) != 0:
            # [for j in range(len(temp_array)) if temp_array[j].split('/')[-1] in mark]
            for j in range(len(temp_array)):
                temp_word_array = temp_array[j].split('/')
                if temp_word_array[-1] in mark:
                    temp_array[j] = '*'
                else:
                    temp_array[j] = temp_word_array[0]
        temp_string = ' '.join(temp_array)
        temp_array = temp_string.split('*')
        # print temp_array
        for k in range(len(temp_array)):
            if temp_array[k] != '' and temp_array[k] != ' ':
                new_data_array.append(temp_array[k].split())
    return new_data_array

if __name__ == '__main__':
    a = ['a/n b/n c/n f/n //w susuu/ws','a/n b/n c/n f/n //w susuu/ws ko/s ','','//w']
    print drop_mark(a)
