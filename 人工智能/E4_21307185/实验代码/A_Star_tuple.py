import numpy as np
from numpy import loadtxt
import copy
from queue import PriorityQueue
from timeit import default_timer as timer

node_num = 0

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
        if(self.fn == other.fn):
            return self.cost < other.cost
        return self.fn < other.fn

def calculate_h(store):
    """计算启发式函数:曼哈顿距离"""
    sum = 0
    for i in range(len(store)):
        if(store[i] == 0):continue
        index1 = (store[i]-1) //4
        index2 = (store[i]-1) % 4
        j = i//4
        k = i%4
        sum += abs(j - index1) + abs(k - index2) 
    return sum

def A_Star(root,initial,close):
    """A*搜索算法"""
    store = PriorityQueue() #创建优先队列
    store.put(root)     #将根节点push进去
    while(not store.empty()):
        global node_num
        node_num += 1
        node = store.get()  #获取f(x) = h(x) + g(x)最小的节点并弹出
        if(node.store == initial):return node #如果找到了目标节点的状态即返回节点
        if(node.store in close):continue
        else :close.add(node.store)
        index = node.store.index(0)   #定位0在二维数组中的位置
        y = index // 4
        x = index % 4
        moves = []
        if x > 0 : moves.append(-1)    # 左移
        if x < 3 : moves.append(+1)    # 右移
        if y > 0 : moves.append(-4)    # 上移
        if y < 3 : moves.append(+4)    # 下移
        
        for m in moves:  
            #生成子节点，进行广度优先搜索（不全是，因为有优先队列的参与，因此可能会回到上一层进行搜索）
            s = list(node.store)
            s[index] = s[index+m]
            s[index+m] = 0
            temp = tuple(s)
            if(temp in close):continue
            hx = calculate_h(temp)
            cur = Node(temp,node,hx,node.level+1)    #创建新的树节点
            if(temp == initial):return cur
            store.put(cur)          #将该新生成的子节点加入优先队列中，进行下一轮的循环

def print_answer(root):
    res = []
    while(root):
        res.append(root.store)
        root = root.parent  #从叶子节点往根节点回溯
    res.reverse()       #反转答案
    s1 = "We tried "+str(len(res)-1)+" times\n"
    line = "---------------\n"
    s2 = "The search time is "+str(toc-tic)+" seconds!\n"
    with open('A_result.txt','w') as f:
        for i in range(len(res)):
            r = np.array(list(res[i])).reshape(4,4)
            f.writelines(str(r))
            if(i>=1):
                f.writelines("   step "+str(i))
            f.writelines('\n'+line)
        f.writelines(s1)
        f.writelines(s2)
    print(node_num)
    
if __name__ == '__main__':
    end_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
    start = loadtxt('test5.txt',dtype = int,delimiter = ',')    #以文件的形式读入初始数组
    close = set()
    start_state = tuple(start.flatten())
    s = Node(start_state,0,calculate_h(start_state),0)   #创建初始根节点
    tic = timer()   #调用测试时间函数进行搜索时间的测量
    root = A_Star(s,end_state,close)
    toc = timer()
    print_answer(root)
