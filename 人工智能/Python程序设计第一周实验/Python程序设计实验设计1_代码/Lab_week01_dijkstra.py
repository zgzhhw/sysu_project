import numpy
from numpy import Infinity
def print_path(parent,start):
    """打印路径
       parent表示父节点数组
       start表示从某个点开始
    """
    store=[]
    index=map_to_int[start]
    if(parent[index]==-1):
        return store
    store.append(start)
    while(parent[index]!=-1):
        #当遇到-1时终止,表示已经到了起点或不能到达
        index=parent[index]
        store.append(map_to_chr[index])
    store.reverse() #反转列表，表示从起点到终点的路径
    return store

map_to_chr={}
map_to_int={}
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

def dijkstra(vertex_num,edge_num,start,end):
    """实现最短路径算法"""
    dis=[Infinity]*vertex_num   #初始化距离数组
    parent=[-1]*vertex_num    #初始化父节点数组，以-1表示终点
    used=[False]*vertex_num     #初始化used数组，确定节点是否被访问
    for i in range(vertex_num):
        graph[i][i]=0 #到自身的距离为零
    dis[map_to_int[start]]=0 #初始化源点的dis为0
    for i in range(vertex_num):
        x = -1
        for y in range(vertex_num):
            if(not used[y] and (x==-1 or dis[y]<dis[x])):
                x = y   #找到dis最小的点
        used[x]=True    #对其进行以访问标记
        for y in range(vertex_num):
            if(dis[y]>dis[x]+graph[x][y]):
                dis[y]=dis[x]+graph[x][y]   #更新距离
                parent[y]=x                 #记录父节点

    distance=dis[map_to_int[end]]
    return [distance,parent]

f=open('test.txt')
s=f.readline()  #读取文件的第一行，获取点数和边数
s=s.split()
vertex_num=int(s[0])
edge_num=int(s[1])
graph=create_graph(f,vertex_num)
while(True):
    #循环输入，当遇到‘#’时退出循环
    ans =input("Please input the start and end:(input '#' exit)\n")
    if(ans=='#'):break
    ans =ans.split()
    start=ans[0]
    end=ans[1]
    if(start not in map_to_int or end not in map_to_int):
        print("Invalid input!")
        continue
    res=dijkstra(vertex_num, edge_num, start, end) #res接受结果,res[0]表示distance; res[1]表示路径
    print("The distance is:",res[0])
    path=print_path(res[1],end)
    if(len(path)==0):
        print("The path is not exist!")
    else :
        for p in path[0:-1]:
            print(p,end="->")
        print(path[-1])
