#coding:utf-8
#version:2.0
#author:fitz_yin

import codecs
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

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

    def drop_mark2(self,dataset):
        mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wn','wm','ws','wp','wb','wh',"tyc"]
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

    def writeMatrix(self, dataset, Path, coding = "utf-8"):
    	for i in xrange(len(dataset)):
    		temp = dataset[i]
    		temp = [str(temp[j]) for j in xrange(len(temp))]
    		temp = ",".join(temp)
    		dataset[i] = temp
    	string = "\n".join(dataset)
    	f = open(Path, "a+")
    	line = f.write(string+"\n")
    	f.close()



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
                wordTemp.append(item["compound_word"])
            dataset = self.UpdateDataset(dataset, wordTemp)
            resultList.append(SingleFP)
        resultListFixed = self.fixResult(resultList)
        return resultListFixed

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
            for item in SingleFP:
                wordTemp.append(item["compound_word"])
            dataset = self.UpdateDataset(dataset, wordTemp)
            resultList.append(SingleFP)
        resultListFixed = self.fixResult(resultList)
        return resultListFixed

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
        return resultListFixed


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
        for i in xrange(len(tempList)):
            for j in xrange(len(tempList)):
                if i == j:
                    pass
                else:
                    if tempList[i]["compound_combined"] in tempList[j]["compound_combined"]:
                        tempList[i]["compound_combined"] = u'*'
        resultList = []
        for i in xrange(len(tempList)):
            if tempList[i]["compound_combined"] != u"*":
                resultList.append(tempList[i])           
        return resultList

    def fix2write(self, dataset):
    	resultType = ["compound_combined","compound_word","num_of_compound_word","num_of_word1","num_of_word2","result"]
    	resultList = []
    	for i in xrange(len(dataset)):
    		temp = []
    		for j in xrange(len(resultType)):
    			temp.append(dataset[i][resultType[j]])
    		resultList.append(temp)
    	return resultList



class CompoundMethod(MiMethod, McMethod, confidenceLevelMethod):
    pass
class DataAnalysis(pretreatment, treatment, CompoundMethod):
    pass



if __name__=='__main__':
    data = DataAnalysis().read_txt('data.txt')
    data = DataAnalysis().drop_mark(data)
    #data = DataAnalysis().drop_mark2(data)
    data = DataAnalysis().make2dList(data)
    #data = DataAnalysis().RemoveStopUseWords(data,'stop_use_words.txt')
    print len(data)
    
    DataAnalysis().writeMatrix([["复旦计算机","句子数量",len(data),"方法","mc","support","10","阈值","0.45"],
    	["复合词","复合词","复合词数量","词1数量","词2数量","方法算出值"]], "result.txt")
#mi
    #resultList = DataAnalysis().MiMethodRe(data, threshold1=20, threshold2=2000)
#mc
    resultList = DataAnalysis().McMethodRe(data, threshold1=10, threshold2=0.45)
#confidenceLevel
    #resultList = DataAnalysis().confidenceLevelMethodRe(data, threshold1=20, threshold2=0.8)
    #print resultList
#dmc
	#resultList = DataAnalysis().McMethodRe(data, threshold1=10, threshold2=0.4)
#support
    #resultList = DataAnalysis().McMethodRe(data, threshold1=10, threshold2=0.0)
    resultList = DataAnalysis().fix2write(resultList)
    print resultList[0]
    DataAnalysis().writeMatrix(resultList,"result.txt")
    