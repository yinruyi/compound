
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
#__________________________________________________________-
#以下模块代码
def remove_stop_use_word(old_tuple):
    stop_use_word=[]
    data=open('stop_use_words.txt','r',encoding= 'utf-8').readlines()
    for i in data:
        if i[-1] == '\n':#去掉回车符号
            i = i[0:-1]
        stop_use_word.append(i)
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
            if supp_zhixindu >= threshold2:
                haha = [k,k,v,supp_huxinxi,supp_mc,dict_list_single[b[0]],dict_list_single[b[1]],supp_zhixindu]
                #result_list.append(k)
                result_list.append(haha)
    return result_list
#-------------------------------------------------------------------
if __name__=='__main__':
    data = []
    data_orgin = open('data.txt','r',encoding= 'utf-8').readlines()
    data = make_tuple(first_fix(data_orgin))
#--------------------------------------------------------------
#以下修改
    list_frequent = []
    list_fre = ['a']#设定初始值
    data = remove_stop_use_word(data)
    length = len(data)
    threshold1,threshold2 = 10,0.45#阈值
    while len(list_fre) > 0:
        list_fre = []
        list_fre = find_frequent_list(data,threshold1,threshold2,length)
        list_haha = []
        for i in list_fre:
            list_haha.append(i[0])    
        data = get_new_data(data,list_haha)
        list_frequent.append(list_fre)
    result_list = fix_result(list_frequent)
    print(str(len(result_list))+'词')
    print('xy,x/y,xy,mi,mc,x,y')
    for i in result_list:
        print(i)
    #print(len(result_list))

    
    