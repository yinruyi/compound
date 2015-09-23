#coding:utf-8
#version:2.0
#author:fitz_yin

import codecs

def first_fix(data):
    mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wn','wm','ws','wp','wb','wh']
    new_data = ' '.join(data)
    fix_data = new_data.split()
    #['1/m', '迪斯尼/nz', '参考/vn', '行程/n', '时间/n', '项目/n']
    for i in range(len(fix_data)):
        b = []
        b = fix_data[i].split('/')
        if len(b) == 2:
            if b[1] in mark :
                fix_data[i] = '*'
            else:
                fix_data[i] = b[0]
        else:
            fix_data[i] = '*'
    #['1', '迪斯尼', '参考', '行程', '时间', '项目', '区域', '游玩', '项目', '备注', '10:00']标点符号全部换成了‘*’
    return fix_data

def make_tuple(data):
    data = ' '.join(data)
    new_data = []
    data = data.split('*')
    for line in data :
        new_line = []
        new_line = line.split()
        new_data.append(new_line)
    return new_data


class pretreatment():
    """预处理"""
    def __init__(self):
        pass
    def read_txt(self,txtPath,coding = 'utf-8'):
        import codecs
        f = codecs.open(txtPath,'r',coding).readlines()
        dataset = []
        for line in f:
            line = line.replace("\r\n","")
            line = line.replace("\n","")
            dataset.append(line)
        return dataset

    def drop_mark(self,dataset):
        mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wn','wm','ws','wp','wb','wh']
        #print mark
        dataset = ' '.join(dataset)
        dataset = dataset.split()
        for i in xrange(len(dataset)):
            temp = []
            temp = dataset[i].split('/')
            if len(temp) == 2:
                if temp[1] in mark:
                    dataset[i] = u'*'
                else:
                    dataset[i] = temp[0]
            else:
                dataset[i] = u'*'
        return dataset

    def make2dList(self, dataset):
        tempString = ' '.join(dataset)
        dataset = tempString.split(u'*')
        tempList = []
        for i in xrange(len(dataset)):
            tempList.append(dataset[i].split())
        resultList = []
        for i in xrange(len(tempList)):
            if tempList[i] != []:
                resultList.append(tempList[i])
        return resultList

    def RemoveStopUseWords(self, dataset, wordPath, coding = 'utf-8'):
        StopUseWords = self.read_txt(wordPath,coding)
        for line in dataset:
            if len(line) == 1:
                if line[0] in StopUseWords:
                    line[0] = u"*"
            else:
                for i in xrange(len(line)):
                    if line[i] in StopUseWords:
                        line[i] = u"*"
        return dataset

class MiMethod():
    """docstring for MiMethod"""
    def __init__(self):
        pass

    def MiMethodFP(self, dataset, threshold1, threshold2):
        #互信息方法
        SingleList, CoupleList = [],[]
        for line in dataset:
            if len(line) == 1:
                SingleList.append(line[0])
            else:
                for i in range(len(line)):
                    SingleList.append(line[i])
                for j in xrange(len(line)-1):
                    CoupleList.append(line[j]+u'/'+line[j+1])
        length = len(dataset)
        SingleDic = self.Counts(SingleList)
        CoupleDic = self.Counts(CoupleList)
        #return CoupleDic
        resultList = []
        for compound,num in CoupleDic.items():
            if num >= threshold1:
                temp = compound.split(u'/')
                supp_mi = 1.0*num*length/(SingleDic[temp[0]]*SingleDic[temp[1]])
                if supp_mi >= threshold2:
                    resultTemp = {"compound_word":compound,"num_of_compound_word":num,"mi":supp_mi}
                    resultTemp["num_of_word1"] = SingleDic[temp[0]]
                    resultTemp["num_of_word2"] = SingleDic[temp[1]]
                    resultList.append(resultTemp)
        return resultList

    def MiMethodRe(self, dataset, threshold1, threshold2):
        SingleFP = ['a']#init
        while len(SingleFP) != 0:
            SingleFP = 0
            pass





       

class treatment():
    def __init__():
        pass
    def writeString(self,string,txtPath = 'out.txt'):
        #将String写入文件
        f = open(txtPath, "a+")
        line = fo.write(string + '\n')
        f.close
    
    def Counts(self, datalist):
        #对List计数
        counts = {}
        for i in datalist:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        return counts


#__________________________________________________________-
#以下模块代码
def remove_stop_use_word(old_tuple):
    stop_use_word=[]
    data = codecs.open('stop_use_words.txt','r','utf-8').readlines()
    for i in data:
        if i[-1] == '\n':#去掉回车符号
            i = i[0:-1]
        stop_use_word.append(i)
    print stop_use_word

    for line in old_tuple:
        if len(line)==1:
            if line[0] in stop_use_word:
                line[0]='*'
        else:
            for i in range(len(line)):
                if line[i] in stop_use_word:
                    line[i]='*'
    return old_tuple

def find_frequent_list(data,threshold1,threshold2,length):
    list_single_data,list_couple_data=get_single_couple_list(data)
    list_fre=over_threshold_select(list_single_data,list_couple_data,threshold1,threshold2,length)
    return list_fre
def get_single_couple_list(data_list):
    list_single=[]
    list_couple=[]
    for line in data_list:
        if len(line)==1:
            list_single.append(line[0])
        else:
            for i in range(len(line)):
                list_single.append(line[i])
    for line in data_list:
        if len(line)==1:
            pass
        else:
            for j in range(len(line)-1):
                list_couple.append(line[j]+'/'+line[j+1])
    return list_single,list_couple
def get_new_data(data,frequent_list):
    new_list=[]
    for item in frequent_list:
        new_list.append(item.split('/'))
    #print(new_list)
    for i in range(len(frequent_list)):
        for line in data:
            if len(line)==1:
                pass
            else:
                for j in range((len(line)-1)):
                    if line[j]==new_list[i][0] and line[j+1]==new_list[i][1]:
                        line[j]=line[j]+line[j+1]
                        #line.insert(j,line[j]+line[j+1])
                        #line.pop([j+1])
                        line[j+1]='*'
    #new_data=[]
    new_data=wipe_out_figure(data, '*')
    return new_data
def count_list_fix(data_list):
    dict_list={}
    data_list_fix=sorted(data_list)
    k=0
    for i in range(1,len(data_list_fix)):
        item=data_list_fix[k]
        if i == len(data_list_fix):
            dict_list[item]=i-k+1
        if  item==data_list_fix[i]:
            pass
        else:
            dict_list[item]=i-k
            k=i
    return dict_list
def get_counts(data_list):
    counts = {}
    for i in data_list:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    return counts
def wipe_out_figure(old_tuple,figure):
    new_tuple=[]
    for line in old_tuple:
        if len(line)==1:
            if line[0]==figure:
                pass
            else:
                new_tuple.append(line)
        else:
            new_line=[]
            for i in range(len(line)):
                if line[i]==figure:
                    pass
                else:
                    new_line.append(line[i])
            new_tuple.append(new_line)
    return new_tuple
def fix_result(old_list):
    data = []
    if len(old_list[0]) == 0:
        return data
    for line in old_list:
        if len(line) == 0:
            pass
        else:
            for i in range(len(line)):
                if '*' in line[i][0] :
                    pass
                else:
                    data.append(line[i])
    #data=[''.join(i.split('/')) for i in data]
    for i in data:
        i[0] = ''.join(i[0].split('/'))
    for i in range(len(data)):
        for j in range(len(data)):
            if i==j:
                pass
            else:
                if data[i][0] in data[j][0] :
                    data[i] = '*'
    #data=[data[i] if data[i] !='*'  for i in range(len(data))]
    new_data=[]
    for i in range(len(data)):
        if data[i] != '*':
            new_data.append(data[i])
    return new_data

def over_threshold_select(list_single,list_couple,threshold1,threshold2,length):
    dict_list_single = get_counts(list_single)
    dict_list_couple = get_counts(list_couple)
    result_list=[]
    for k,v in dict_list_couple.items():
        if v>=threshold1:
            haha = []
            b = k.split('/')
            supp_huxinxi = v*length/(dict_list_single[b[0]]*dict_list_single[b[1]])
            #互信息公式
            supp_mc = v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            #mc公式
            supp_new = 0.4*(v/(10+v))+0.6*v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            #xinfangfa
            supp_zhixindu = v/dict_list_single[b[0]]
            supp_yuan = v*v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            #tf平方/min(tf1,tf2)
            supp_er = v*v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            if supp_mc >= threshold2:
                haha = [k,k,v,supp_huxinxi,supp_mc,dict_list_single[b[0]],dict_list_single[b[1]],supp_er]
                #result_list.append(k)
                result_list.append(haha)
    return result_list

#-------------------------------------------------------------------
class DataAnalysis(pretreatment,treatment,MiMethod):
    pass


if __name__=='__main__':
    data = DataAnalysis().read_txt('data.txt')
    data = DataAnalysis().drop_mark(data)
    data = DataAnalysis().make2dList(data)
    data = DataAnalysis().RemoveStopUseWords(data,'stop_use_words.txt')
    #print data
    a = DataAnalysis().MiMethodFP(data, threshold1=10, threshold2=100)
    print a


    #print first_fix(data)

    '''
    print data[0]
    print len(data)
    data = make_tuple(first_fix(data))
    print data[0]

#--------------------------------------------------------------
#以下修改
    list_frequent = []
    list_fre = ['a']#设定初始值
    data = remove_stop_use_word(data)
    length = len(data)
    threshold1,threshold2 = 10,0.8#阈值
    while len(list_fre) > 0:
        list_fre = []
        list_fre = find_frequent_list(data,threshold1,threshold2,length)
        list_haha = []
        for i in list_fre:
            list_haha.append(i[0])    
        data = get_new_data(data,list_haha)
        list_frequent.append(list_fre)
    result_list = fix_result(list_frequent)
    for i in result_list:
        print(i)
    print(len(result_list))
    '''

    
    