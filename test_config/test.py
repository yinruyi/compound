# -* - coding: UTF-8 -* -
import ConfigParser
#生成config对象
conf = ConfigParser.ConfigParser()
#用config对象读取配置文件
conf.read("test.cfg")
#以列表形式返回所有的section
sections = conf.sections()
print 'sections:', sections         #sections: ['sec_b', 'sec_a']
#得到指定section的所有option
options = conf.options("sec_a")
print 'options:', options           #options: ['a_key1', 'a_key2']
#得到指定section的所有键值对
kvs = conf.items("sec_a")
print 'sec_a:', kvs                 #sec_a: [('a_key1', '20'), ('a_key2', '10')]
#指定section，option读取值
str_val = conf.get("sec_a", "a_key1")
int_val = conf.getint("sec_a", "a_key2")

print "value for sec_a's a_key1:", str_val   #value for sec_a's a_key1: 20
print "value for sec_a's a_key2:", int_val   #value for sec_a's a_key2: 10

#写配置文件
#更新指定section，option的值
#conf.set("sec_b", "b_key3", "new-$r")
#写入指定section增加新option和值
#conf.set("sec_b", "b_newkey", "new-value")
#增加新的section
#conf.add_section('a_new_section')
#conf.set('a_new_section', 'new_key', 'new_value')
#写回配置文件
#conf.write(open("test.cfg", "w"))
