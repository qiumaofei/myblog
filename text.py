# list = [15,3,59,88,77,34]

#
# #冒泡
# for out in range(len(list)-1):
#     #每一次都是从索引0开始的  循环的次数 = len(list0) - 第几次遍历out
#     for inner in range(len(list) - out -1):
#         if list[inner] > list[inner + 1]:
#             list[inner], list[inner+1] = list[inner + 1], list[inner]
#
# #排好序了
# print(list)
#
# #选择
# for i in range(len(list)-1,0,-1):
#     for j in range(i):
#         if list[j] > list[i]:
#             list[j],list[i] = list[i],list[j]
# print(list)
#
# #插入
# for i in range(1,len(list)):
#     for j in range(i,0,-1):
#         if list[j] < list[j-1]:
#             list[j],list[j-1] = list[j-1],list[j]
# print(list)
###############################################################

# def func(a,n):
#     b = []
#
#     for i in a:
#         if a.count(i) > n:
#             b.append(i)
#     b = list(set(b))
#     return b
# print(func(a= [1,3,2,4,3,1],n= 1))

###################################################################
s = 'love_you_ying'
# s3 = s.title()
# s1 = s.split('_')
# s2 = s3.replace('_','')
# print(s2)
s1 = s.split('_')
s2 = ''
stwo = s1[1].title()
sthree = s1[2].title()
print(s1[1] + stwo + sthree)


