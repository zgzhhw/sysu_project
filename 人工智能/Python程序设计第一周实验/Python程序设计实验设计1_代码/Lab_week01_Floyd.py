import numpy
from numpy import Infinity
map_to_chr={}# 创建字典将整数映射到字符
map_to_int={}# 创建字典将字符映射到整数
def create_graph(f,vertex_num):
    """创建无向图"""
    graph=[[Infinity]*vertex_num for _ in range(vertex_num)] #用列表解析式初始化图
    #graph=numpy.full((vertex_num,vertex_num),Infinity) #调用numpy创建二维数组
    k=0
    for line in f.readlines():
        """逐行读取文件，创建无向图"""
        line=line.strip()
        print(line)
        s=line.split( ) #分割空格
        weight=int(s[2])
        if(s[0] not in map_to_int):
            map_to_int[s[0]]=k
            map_to_chr[k]=s[0]
            k+=1
        if(s[1] not in map_to_int):
            map_to_int[s[1]]=k
            map_to_chr[k]=s[1]
            k+=1
        graph[map_to_int[s[0]]][map_to_int[s[1]]]=weight
        graph[map_to_int[s[1]]][map_to_int[s[0]]]=weight
    return graph
    
def print_path(path,start,end):
    print("The path is:",end="")#避免换行
    while(start!=end): #判断是否到达终点
        print(map_to_chr[start],end="->")
        start=path[start][end]
    print(map_to_chr[end])

def Floyd(graph,path):
    for i in range (vertex_num):
        for j in range (vertex_num):
            for k in range (vertex_num):
                if (graph[j][k]>graph[j][i]+graph[i][k]):
                    graph[j][k]=graph[j][i]+graph[i][k] #更新中间节点的距离
                    path[j][k]=path[j][i]               #更新路径到中间节点
    
f=open('test.txt')
s=f.readline()  #读取文件的第一行，获取点数和边数
s=s.split()
vertex_num=int(s[0])
edge_num=int(s[1])
graph=create_graph(f,vertex_num)
path = [[Infinity]*vertex_num for _ in range(vertex_num)]
for i in range (vertex_num):
    for j in range (vertex_num):
        path[i][j]=j    #初始化path二维数组
Floyd(graph,path)       #调用Floyd算法求最短路径
while True:             #循环输入，当输入'#'时终止
    s =input("Please input the start and end:(input '#' exit)\n")
    if(s=='#'):break
    s=s.split()
    if(s[0] not in map_to_int or s[1] not in map_to_int):
        print("Invalid input!")
        continue
    start = map_to_int[s[0]]
    end = map_to_int[s[1]]
    print("The distance is:",graph[start][end]) #打印最短距离
    print_path(path,start,end)                  #打印最短路径
