#删除停用词，互信息
def first_fix(data):
    mark = ['w','wkz','wky','wyz','wyy','wj','ww','wt','wd','wf','wn','wm','ws','wp','wb','wh']
    wipe = open('cixing.txt','r',encoding= 'utf-8').readline()
    wipe_word = wipe.split()
    #停用词性
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
                if b[1] in wipe_word :
                    fix_data[i] = '&'
                else:
                    fix_data[i] = b[0]
        else:
            fix_data[i] = '*'
    #['1', '迪斯尼', '参考', '行程', '时间', '项目', '区域', '游玩', '项目', '备注', '10:00']标点符号全部换成了‘*’
    return fix_data

def make_fast(data):
    new_data=[]
    fix_data=[]
    for line in data :
        a = ' '.join(line)
        new_data.append(a)
    new_line = '*'.join(new_data)
    a = new_line.split('& &')
    while len(a) >1 :
        new_line = '&'.join(a)
        a = new_line.split('& &')
    b = new_line.split('*')
    for i in b :
        fix_line = []
        fix_line = i.split()
        fix_data.append(fix_line)
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

#-------------------------------------------------------------------


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

def over_threshold_select(list_single,list_couple,threshold1,threshold2,length):
    #time1=time.time()
    dict_list_single=count_list_fix(list_single)
    dict_list_couple=count_list_fix(list_couple)
    #time2=time.time()
    #print(time2-time1)
    result_list=[]
    for k,v in dict_list_couple.items():
        if v>=threshold1:
            b=k.split('/')
            supp_huxinxi = v*length/(dict_list_single[b[0]]*dict_list_single[b[1]])
            #互信息公式
            supp_mc = v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            #mc公式
            #supp_new = 0.4*(v/(10+v))+0.6*v/min(dict_list_single[b[0]],dict_list_single[b[1]])
            #xinfangfa
            #supp_zhixindu = v/dict_list_single[b[0]]
            if supp_mc >= threshold2:
                haha = [k,k,v,supp_huxinxi,supp_mc,dict_list_single[b[0]],dict_list_single[b[1]]]
                #result_list.append(k)
                result_list.append(haha)
    return result_list

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
    data=[]
    if len(old_list[0]) == 0:
        return data
    for line in old_list:
        if len(line) == 0:
            pass
        else:
            for i in range(len(line)):
                if '*' in line[i][0] :#修改过
                    pass
                else:
                    if '&' in line[i][0]:
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



#-------------------------------------------------------------------

if __name__=='__main__':
    data = []
    data_orgin = open('data.txt','r',encoding= 'utf-8').readlines()
    data = make_tuple(first_fix(data_orgin))
    line = make_fast(data)
    length = len(data)
    #print(line[0:100])
    
#-------------------------------------------------------
#以下修改
    list_frequent = []
    list_fre = ['a']#设定初始值
    threshold1,threshold2 = 10,0#阈值
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
    write_file=open('out.txt','w',encoding= 'utf-8')
    for i in result_list:
        print(i)
        jj = str(i)
        kk = ','.join(jj)
        write_file.writelines(str(kk))
        write_file.writelines('\n')
    write_file.close()
    
    