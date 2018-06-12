from urllib.request import urlopen

list1 = ['a', 'a', 'b', 'c', 'd', 'c']
print(type(list1))

# 列表转集合
set1 = set(list1)
print(set1)
print(type(set1))

# 列表转元组
tuple1 = tuple(list1)
print(tuple1)
print(type(tuple1))


tuple2 = ('1', '2', '1', 'a', 'v', 'e', 'a')

# 元组转列表
list2 = list(tuple2)
print(list2)
print(type(list2))

# 元组转集合（集合：去重、无序）
set2 = set(tuple2)
print(set2)
print(type(set2))

set3 = {'a', 'b', 'c', 'd'}

# 集合转列表
list3 = list(set3)
print(list3)
print(type(list3))

# 集合转元组
tuple3 = tuple(set3)
print(tuple3)
print(type(tuple3))

# dict1 = dict(list1[1])
# print(dict1)


base_url = 'http://sports.sohu.com/nba_a.shtml'
# 抓取页面
get_url = urlopen(base_url)
print(get_url)
# 读取页面,读出的数据是byte类型, 并且是一行输出
read_url = get_url.read()
print(read_url)
# 页面解码
decode_page = read_url.decode('gbk')
# 创建soup对象

# print(decode_page)

