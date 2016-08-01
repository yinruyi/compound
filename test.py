# -*- coding: utf-8 -*-

import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class baseMethod(object):
    def __init__(self):
        super(baseMethod, self).__init__()

    def drop_mark(self, data_array):
        mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt',\
                'wd','wf','wn','wm','ws','wp','wb','wh',"tyc"]
        new_data_array = []
        for i in range(len(data_array)):
            temp_array = data_array[i].split()

    def array_counts(self, data_array):
        counts = {}
        for i in data_array:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        return counts

    def drop_mark_stopword(self, data_array):
        pass

    def get_single_couple_dict(self, dataset):
        SingleList, CoupleList = [],[]
        for line in dataset:
            if len(line) == 1:
                SingleList.append(line[0])
            else:
                for i in range(len(line)-1):
                    SingleList.append(line[i])
                    CoupleList.append(line[i]+u'/'+line[i+1])
                SingleList.append(len(line)-1)
        print self.array_counts(SingleList), self.array_counts(CoupleList)
        return self.array_counts(SingleList), self.array_counts(CoupleList)

if __name__ == '__main__':
	a = ['a ng e w fd sd a dwe','ew re q  dsf we  tert a a a a a']
	baseMethod().get_single_couple_dict(a)