# -*- coding: utf-8 -*-

def test_drop_mark(data_array):
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

def test_list_split(array, split_string='*'):
    temp_string = ' '.join(array)
    split_string = ' ' + split_string
    temp_array = temp_string.split(split_string)
    return [temp_array[i].split() for i in range(len(temp_array))]

def test_remove_stopwords(data_array):
    def list_split(array, split_string='*'):
        temp_string = ' '.join(array)
        # split_string = ' ' + split_string
        temp_array = temp_string.split(split_string)
        return [temp_array[i].split() for i in range(len(temp_array))]

    result_data_array = []
    # stopwords = InputOutput().read_txt(stopwords_path, coding)
    stopwords = ['sdio','ewio','n','d']
    for i in range(len(data_array)):
        if data_array[i] != []:
            for j in range(len(data_array[i])):
                if data_array[i][j] in stopwords:
                    data_array[i][j] = '*'
            print data_array[i]
            print list_split(data_array[i])
            result_data_array.extend(filter(lambda x:x, list_split(data_array[i])))
    return result_data_array

def test_iteritems():
    a = {'a':1,'b':2}
    for k,v in a.iteritems():
        print k,v

class TestClass():  
    def sub(self,a,b):  
        return a-b  
    def add(self,a,b):  
        return a+b  
    def echo(self):  
        print "test"  

class Data(object):
    def __init__(self, module_name, class_name):
        self.module_name = module_name
        self.class_name = class_name
        self = getattr(module_name, class_name)
 
def main():  
    class_name = "TestClass" #类名  
    module_name = "test"   #模块名  
    method = "echo"          #方法名  
  
    module = __import__(module_name) # import module  
    print "#module:",module  
    c = getattr(module,class_name)    
    print "#c:",c,type(c) 
    obj = c() # new class  
    print "#obj:",obj  
    print(obj)  
    obj.echo()  
    mtd = getattr(obj,method)  
    print "#mtd:",mtd  
    mtd() # call def  
      
    mtd_add = getattr(obj,"add")  
    t=mtd_add(1,2)  
    print "#t:",t  
  
    mtd_sub = getattr(obj,"sub")  
    print mtd_sub(2,1)  


def test_thread(data_array, word_list):

    def test_update_line(line):
        if len(line) == 1:
            return line
        else:
            for i in range(len(word_list)):
                for j in range(len(line)-1):
                    if line[j] == word_list[i][0] and line[j+1] == word_list[i][1]:
                        line[j] = line[j] + line[j+1]
                        line[j+1] = ''
            return line

    print data_array
    IS_MUTI_THREAD = True
    MUTI_THREAD_NUM = 3
    if IS_MUTI_THREAD:
        from multiprocessing.dummy import Pool as ThreadPool
    if IS_MUTI_THREAD:
        pool = ThreadPool(MUTI_THREAD_NUM)
        pool.map(test_update_line, data_array)
        data_array = [filter(lambda x:x!='',line) for line in data_array]
    else:
        # for i in range(len(data_array)):
            # data_array[i] = filter(lambda x:x!='', test_update_line(data_array[i]))
        data_array = [filter(lambda x:x!='', test_update_line(line)) for line in data_array]

    print data_array

if __name__ == '__main__':
    # a = ['a/n b/n c/n f/n //w susuu/ws','a/n b/n c/n f/n //w susuu/ws ko/s ','','//w']
    # # print drop_mark(a)
    # b = ['a','*','d','d','s','*']
    # result = list_split(b)
    # print result
    # result = filter(lambda x:x, result)
    # print result
    # a = [['n','ds','dwe','d','we','weweas','d'],['we','wqe','d','wqe','ewqewq','d']]
    # print test_remove_stopwords(a)
    # test_iteritems()
    # main()
    # d = Data('test', 'TestClass')
    # print d
    word_list = [['a','b'],['k','b'],['h','o']]
    data_array = [['a','d','k','b','w','h','o'],['a','b'],[',','h','o']]
    test_thread(data_array, word_list)

