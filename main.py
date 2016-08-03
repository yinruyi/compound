# -*- coding: utf-8 -*-

import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


class InputOutput(object):
    def __init__(self):
        super(InputOutput, self).__init__()

    def read_txt(self, txtPath, coding = 'utf-8')
        f = codecs.open(txtPath,'r',coding).readlines()
        f[0] = f[0].replace(u"\ufeff",u"")
        dataset = []
        for line in f:
            line = line.replace("\r\n","")
            line = line.replace("\n","")
            dataset.append(line)
        return dataset

    def writeMatrix(self, dataset, Path, coding = "utf-8"):
        for i in range(len(dataset)):
            temp = dataset[i]
            temp = [str(temp[j]) for j in xrange(len(temp))]
            temp = ",".join(temp)
            dataset[i] = temp
        string = "\n".join(dataset)
        f = open(Path, "a+")
        line = f.write(string+"\n")
        f.close()


class PreProcess(object):
    def __init__(self):
        super(PreProcess).__init__()

    def drop_mark(self, data_array):
        mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt',\
                'wd','wf','wn','wm','ws','wp','wb','wh','tyc']
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
            for k in range(len(temp_array)):
                if temp_array[k] != '' and temp_array[k] != ' ':
                    new_data_array.append(temp_array[k].split())
        return new_data_array

    def drop_mark_stopword(self, data_array):
        mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wn',\
                'wm','ws','wp','wb','wh','tyc','t', 'tg', 'f', 'r', 'rr',\
                'rz', 'rzt', 'rzs', 'rzv', 'ry', 'ryt', 'rys', 'ryv', 'rg',\
                'm', 'mq', 'q', 'qv', 'qt', 'd', 'p', 'pba', 'pbei', 'c',\
                'cc', 'u', 'uzhe', 'ule', 'uguo', 'ude1', 'ude2', 'ude3',\
                'usuo', 'udeng', 'uyy', 'udh', 'uls', 'uzhi', 'ulian', 'e',\
                'y', 'o', 'x', 'xx', 'xu']       
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
            for k in range(len(temp_array)):
                if temp_array[k] != '' and temp_array[k] != ' ':
                    new_data_array.append(temp_array[k].split())
        return new_data_array

    def remove_stopwords(self, data_array, stopwords_path, coding='utf-8'):
        def list_split(array, split_string='*'):
            temp_string = ' '.join(array)
            temp_array = temp_string.split(split_string)
            return [temp_array[i].split() for i in range(len(temp_array))]

        result_data_array = []
        stopwords = InputOutput().read_txt(stopwords_path, coding)
        for i in range(len(data_array)):
            if data_array[i] != []:
                for j in range(len(data_array[i])):
                    if data_array[i][j] in stopwords:
                        data_array[i][j] = '*'
                result_data_array.extend(filter(lambda x:x, list_split(data_array[i])))
        return result_data_array


class BaseMethod(PreProcess):
    def __init__(self):
        super(BaseMethod, self).__init__()

    def array_counts(self, data_array):
        counts = {}
        for i in data_array:
            if i in counts:
                counts[i] += 1
            else:
                counts[i] = 1
        return counts

    def get_single_couple_dict(self, dataset):
        single_list, couple_list = [],[]
        for line in dataset:
            if len(line) == 1:
                single_list.append(line[0])
            else:
                for i in range(len(line)-1):
                    single_list.append(line[i])
                    couple_list.append(line[i]+u'/'+line[i+1])
                single_list.append(len(line)-1)
        return self.array_counts(single_list), self.array_counts(couple_list)

    def find_compound_word(self, dataset, threshold_1, threshold_2):
        single_dict,couple_dict = self.get_single_couple_dict(dataset)
        


class MiMethod(baseMethod):
    """mi/互信息方法
    """
    def __init__(self):
        super(MiMethod, self).__init__()

    def find_compound_word(self, dataset, threshold_1, threshold_2):
        single_dict,couple_dict = self.get_single_couple_dict(dataset)
        result_list = []
        for compound_word_candidate, num in couple_dict.iteritems():
            if num >= threshold_1:
                compound_two_word = compound_word_candidate.split('/')
                supp_mi = 1.0*num*length/(single_dict[compound_two_word[0]]*\
                    single_dict[compound_two_word[1]])
                if supp_mi >= threshold_2:
                    result_temp = {'compound_word' : compound_word_candidate,\
                        'num_of_compound_word' : num, 'result' : supp_mi}
                    result_temp['num_of_word_1'] = single_dict[compound_two_word[0]]
                    result_temp['num_of_word_2'] = single_dict[compound_two_word[1]]
                    result_temp['compound_word'] = compound_two_word[0] + \
                                                   compound_two_word[1]
                    result_list.append(result_temp)
        return result_list
        
#-------------------------------------------------------------------        

class MiMethod():
    """mi/互信息方法"""
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
                    resultTemp = {"compound_word":compound,"num_of_compound_word":num,"result":supp_mi}
                    resultTemp["num_of_word1"] = SingleDic[temp[0]]
                    resultTemp["num_of_word2"] = SingleDic[temp[1]]
                    resultTemp["compound_combined"] = temp[0]+temp[1]
                    resultList.append(resultTemp)
        return resultList

    def MiMethodRe(self, dataset, threshold1, threshold2):
        SingleFP = ['a']#init
        resultList = []
        while len(SingleFP) != 0:
            SingleFP = self.MiMethodFP(dataset, threshold1, threshold2)
            wordTemp = []
            for item in SingleFP:
                #print type(item)
                wordTemp.append(item["compound_word"])
            dataset = self.UpdateDataset(dataset, wordTemp)
            resultList.append(SingleFP)
        resultListFixed = self.fixResult(resultList)
        return resultListFixed,dataset

class McMethod():
    """mc/最大置信度方法"""
    def __init__(self):
        pass

    def McMethodFP(self, dataset, threshold1, threshold2):
        #最大置信度方法
        SingleList, CoupleList = [],[]
        for line in dataset:
            if len(line) == 1:
                SingleList.append(line[0])
            else:
                for i in range(len(line)):
                    SingleList.append(line[i])
                for j in xrange(len(line)-1):
                    CoupleList.append(line[j]+u'/'+line[j+1])
        #length = len(dataset)
        SingleDic = self.Counts(SingleList)
        CoupleDic = self.Counts(CoupleList)
        #return CoupleDic
        resultList = []
        for compound,num in CoupleDic.items():
            if num >= threshold1:
                temp = compound.split(u'/')
                supp_mc = 1.0*num/min(SingleDic[temp[0]],SingleDic[temp[1]])
                if supp_mc >= threshold2:
                    resultTemp = {"compound_word":compound,"num_of_compound_word":num,"result":supp_mc}
                    resultTemp["num_of_word1"] = SingleDic[temp[0]]
                    resultTemp["num_of_word2"] = SingleDic[temp[1]]
                    resultTemp["compound_combined"] = temp[0]+temp[1]
                    resultList.append(resultTemp)
        return resultList

    def McMethodRe(self, dataset, threshold1, threshold2):
        SingleFP = ['a']#init
        resultList = []
        while len(SingleFP) != 0:
            SingleFP = self.McMethodFP(dataset, threshold1, threshold2)
            wordTemp = []
            #print type(SingleFP[0])
            for item in SingleFP:
                #print item
                wordTemp.append(item["compound_word"])
            dataset = self.UpdateDataset(dataset, wordTemp)
            resultList.append(SingleFP)
        resultListFixed = self.fixResult(resultList)
        return resultListFixed,dataset

class confidenceLevelMethod():
    """confidenceLevel/置信度方法"""
    def __init__(self):
        pass

    def confidenceLevelMethodFP(self, dataset, threshold1, threshold2):
        #置信度方法
        SingleList, CoupleList = [],[]
        for line in dataset:
            if len(line) == 1:
                SingleList.append(line[0])
            else:
                for i in range(len(line)):
                    SingleList.append(line[i])
                for j in xrange(len(line)-1):
                    CoupleList.append(line[j]+u'/'+line[j+1])
        #length = len(dataset)
        SingleDic = self.Counts(SingleList)
        CoupleDic = self.Counts(CoupleList)
        #return CoupleDic
        resultList = []
        for compound,num in CoupleDic.items():
            if num >= threshold1:
                temp = compound.split(u'/')
                supp_cl = 1.0*num/SingleDic[temp[0]]
                if supp_cl >= threshold2:
                    resultTemp = {"compound_word":compound,"num_of_compound_word":num,"result":supp_cl}
                    resultTemp["num_of_word1"] = SingleDic[temp[0]]
                    resultTemp["num_of_word2"] = SingleDic[temp[1]]
                    resultTemp["compound_combined"] = temp[0]+temp[1]
                    resultList.append(resultTemp)
        return resultList

    def confidenceLevelMethodRe(self, dataset, threshold1, threshold2):
        SingleFP = ['a']#init
        resultList = []
        while len(SingleFP) != 0:
            SingleFP = self.confidenceLevelMethodFP(dataset, threshold1, threshold2)
            wordTemp = []
            for item in SingleFP:
                wordTemp.append(item["compound_word"])
            dataset = self.UpdateDataset(dataset, wordTemp)
            resultList.append(SingleFP)
        resultListFixed = self.fixResult(resultList)
        return resultListFixed,dataset


class treatment():
    '''处理程序'''
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

    def UpdateDataset(self, dataset, FPList):
        FP2DList = []
        for item in FPList:
            FP2DList.append(item.split(u'/'))
        for i in xrange(len(FP2DList)):
            for line in dataset:
                if len(line) == 1:
                    pass
                else:
                    for j in xrange(len(line)-1):
                        if line[j] == FP2DList[i][0] and line[j+1] == FP2DList[i][1]:
                            line[j] = line[j]+line[j+1]
                            line[j+1] = u'*'
        UpDataset = []
        for line in dataset:
            if len(line) == 1:
                if line[0] == u'*':
                    pass
                else:
                    UpDataset.append(line)
            else:
                tempList = []
                for i in xrange(len(line)):
                    if line[i] == u'*':
                        pass
                    else:
                        tempList.append(line[i])
                UpDataset.append(tempList)
        return UpDataset

    def fixResult(self, dataset):
        tempList = []
        if len(dataset) == 1:
            return []
        else:
            for i in xrange(len(dataset)):
                if len(dataset[i]) == 0:
                    pass
                else:
                    for j in xrange(len(dataset[i])):
                        if u'*' in dataset[i][j]["compound_word"]:
                            pass
                        else:
                            tempList.append(dataset[i][j])
        #for i in xrange(len(tempList)):
        #    for j in xrange(len(tempList)):
        #        if i == j:
        #            pass
        #        else:
        #            if tempList[i]["compound_combined"] in tempList[j]["compound_combined"]:
        #                tempList[i]["compound_combined"] = u'*'
        #resultList = []
        #for i in xrange(len(tempList)):
        #    if tempList[i]["compound_combined"] != u"*":
        #        resultList.append(tempList[i])
        resultList = tempList          
        return resultList
    def compare2getResult(self, data, dataset, tempList, threshold1):
        temp_resultList = []
        resultList = []
        result = []
        for i in xrange(len(dataset)):
            if len(data[i]) == len(dataset[i]):
                pass
            else:
                temp = dataset[i]
                if len(temp) != 0:
                    for j in xrange(len(temp)):
                        if temp[j] not in data[i]:
                            temp_resultList.append(temp[j])
        temp_resultList = self.Counts(temp_resultList)
        #print len(temp_resultList)
        for k,v in temp_resultList.items():
            if v >= threshold1:
                resultList.append(k)
        #print len(resultList)
        for i in xrange(len(tempList)):
            if tempList[i]["compound_combined"] in resultList:
                result.append(tempList[i])
        #print result,len(result)
        return result

    def fix2write(self, dataset):
        resultType = ["compound_combined","compound_word","num_of_compound_word","num_of_word1","num_of_word2","result"]
        resultList = []
        for i in xrange(len(dataset)):
            temp = []
            for j in xrange(len(resultType)):
                #print dataset[i],resultType[j]
                temp.append(dataset[i][resultType[j]])
            resultList.append(temp)
        return resultList








class CompoundMethod(MiMethod, McMethod, confidenceLevelMethod):
    pass
class DataAnalysis(pretreatment, treatment, CompoundMethod):
    pass

def preData(path):
    #数据预处理
    data = DataAnalysis().read_txt('data.txt')
    data = DataAnalysis().drop_mark(data)
    data = DataAnalysis().make2dList(data)
    return data
def d_preData(path):
    #删词性的预处理
    data = DataAnalysis().read_txt('data.txt')
    data = DataAnalysis().drop_mark2(data)
    data = DataAnalysis().make2dList(data)
    return data

def main(path, method, threshold1, threshold2=0):
    writePath = "result.txt"
    if method == "mi":
        data = preData(path)
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().MiMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")
    elif method == "mc":
        data = preData(path)
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().McMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")
    elif method == "confidence":
        data = preData(path)
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().confidenceLevelMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")
    elif method == "dmc":
        data = d_preData(path)
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().McMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")
    elif method == "support":
        data = preData(path)
        threshold2 = 0
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().McMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")
    elif method == "dsupport":
        data = d_preData(path)
        threshold2 = 0
        DataAnalysis().writeMatrix([["句子数量",len(data),"方法",method,"support",threshold1,"阈值",threshold2],
            ["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], writePath)
        tempList, dataset = DataAnalysis().McMethodRe(data, threshold1, threshold2)
        resultList = DataAnalysis().compare2getResult(preData(path), dataset, tempList, threshold1)
        resultList = DataAnalysis().fix2write(resultList)
        DataAnalysis().writeMatrix(resultList,"result.txt")


if __name__=='__main__':
    #main("data.txt", "mi",5,300)
    #main("data.txt","mc",20,0.8)
    #main("data.txt","confidence",20,0.8)
    #main("data.txt","dmc",20,0.8)
    #main("data.txt","support",20)
    #main("data.txt","dsupport",20)