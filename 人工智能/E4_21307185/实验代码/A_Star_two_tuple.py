import numpy as np
from numpy import loadtxt
import copy
from queue import PriorityQueue
from timeit import default_timer as timer

map1 = {}
map2 = {}
class Node:
    """定义搜索的节点"""
    def __init__(self,s,parent = 0,cost = 0,level = 0):
        self.store = s          #存储二维数组表示状态
        self.parent = parent    #存储节点的父亲节点，方便回溯
        self.cost = cost        #存储h(x)的计算结果
        self.level = level      #存储g(x)的计算结果
        self.fn = self.level + self.cost
    
    def __lt__(self,other):
        """定义内置比较函数,优先队列可以根据该函数进行优先级的判定"""
        if(self.fn == other.fn ):
            return self.cost < other.cost
        return self.fn < other.fn

def calculate_h(start,target):
    """计算启发式函数:曼哈顿距离"""
    sum = 0
    for i in range(len(start)):
        s = start[i]
        if(s == 0):continue
        index = target.index(s)
        j = i // 4
        k = i % 4
        x = index // 4
        y = index % 4
        sum += abs(j-x)+abs(k-y)
    return sum

def swap(s,x,y):
    """自定义交换函数"""
    temp = s[x]
    s[x] = s[y]
    s[y] = temp

def A_Star(root,initial,close,close2):
    """A*搜索算法"""
    store = PriorityQueue() #创建优先队列
    store.put(root)     #将根节点push进去
    close.add(root.store)  #将根节点的字符串表达式加入close集合中，进行环检测
    store2 = PriorityQueue() #创建优先队列
    t = Node(initial,0,calculate_h(root.store, initial),0)
    store2.put(t)     #将根节点push进去
    close2.add(initial)   #将根节点的字符串表达式加入close2集合中，进行环检测
    node = root
    node2 = t
    while(True):
        #print(store.qsize(),store2.qsize())
        node = store.get()  #获取f(x) = h(x) + g(x)最小的节点并弹出
        index = node.store.index(0)
        target = store2.get()
        if(target.store in close):return [map1[target.store],target]
        store2.put(target)
        y = index // 4
        x = index % 4
        moves = []
        if x > 0 and index - 1 >= 0 : moves.append(-1)    # 左移
        if x < 3 and index + 1 < 16 : moves.append(+1)    # 右移
        if y > 0 and index - 4 >= 0 : moves.append(-4)    # 上移
        if y < 3 and index + 4 < 16 : moves.append(+4)    # 下移i 

        for m in moves:  
            #生成子节点，进行广度优先搜索（不全是，因为有优先队列的参与，因此可能会回到上一层进行搜索）
            s = list(node.store)
            swap(s,index,index+m)      #进行交换，相当于移动滑块的操作
            temp = tuple(s)

            if (temp) in close:continue    #进行环检测，如果节点在close中，则跳过
            close.add(temp)                #如果没有则加入
            cur = Node(temp,node,calculate_h(temp,target.store),node.level+1)    #创建新的树节点
            
            map1[temp] = cur
            store.put(cur)          #将该新生成的子节点加入优先队列中，进行下一轮的循环

        node2 = store2.get()  #获取f(x) = h(x) + g(x)最小的节点并弹出
        index2 = node2.store.index(0)
        target2 = store.get()
        if(target2.store in close2):return [target2,map2[target2.store]]
        store.put(target2)
        y = index2 // 4
        x = index2 % 4
        moves = []
        if x > 0 and index2 - 1 >= 0 : moves.append(-1)    # 左移
        if x < 3 and index2 + 1 < 16 : moves.append(+1)    # 右移
        if y > 0 and index2 - 4 >= 0 : moves.append(-4)    # 上移
        if y < 3 and index2 + 4 < 16 : moves.append(+4)    # 下移i 
        for m in moves:  
           #生成子节点，进行广度优先搜索（不全是，因为有优先队列的参与，因此可能会回到上一层进行搜索）
            s = list(node2.store)
            swap(s,index2,index2+m)      #进行交换，相当于移动滑块的操作
            temp = tuple(s)

            if (temp) in close2:continue    #进行环检测，如果节点在close2中，则跳过
            close2.add(temp)                #如果没有则加入
                
            cur2 = Node(temp,node2,calculate_h(temp,target2.store),node2.level+1)    #创建新的树节点
            
            map2[temp] = cur2
            store2.put(cur2)          #将该新生成的子节点加入优先队列中，进行下一轮的循环

end_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
start = loadtxt('test2.txt',dtype = int,delimiter = ',')    #以文件的形式读入初始数组
start_list = []
for i in range(len(start)):
    for j in range(len(start[i])):
        start_list.append(start[i][j])
start_state = tuple(start_list)
close2 = set()
close = set()
s = Node(start_state,0,calculate_h(start_state,end_state),0)   #创建初始根节点
tic = timer()   #调用测试时间函数进行搜索时间的测量
root = A_Star(s,end_state,close,close2)
toc = timer()
res = []

while(root[0]):
    res.append(root[0].store)
    root[0] = root[0].parent  #从叶子节点往根节点回溯
res.reverse()       #反转答案
count = 0
root[1] = root[1].parent
while(root[1]):
    count += 1
    res.append(root[1].store)
    root[1] = root[1].parent

#输出结果
s1 = "We tried "+str(len(res)-1)+" times\n"
line = "---------------\n"
s2 = "The search time is "+str(toc-tic)+" seconds!\n"
with open('A_better2.txt','w') as f:
    for i in range(len(res)):
        r = np.array(list(res[i])).reshape(4,4)
        f.writelines(str(r))
        if(i>=1):
            f.writelines("   step "+str(i))
        f.writelines('\n'+line)
    f.writelines(s1)
    f.writelines(s2)
