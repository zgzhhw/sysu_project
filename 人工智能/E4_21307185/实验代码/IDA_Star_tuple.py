import numpy as np
from numpy import loadtxt
import random
import copy
from queue import PriorityQueue
from timeit import default_timer as timer

path =[]
close = set()
end_state = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0)
#上面的作为全局变量

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

def swap(s,x,y):
    """自定义交换函数"""
    temp = s[x]
    s[x] = s[y]
    s[y] = temp

def dfs(bound,g):
    """迭代加深启发式搜索"""
    node = path[-1]     #获取路径上的最后一个节点
    expense = g + calculate_h(node)      #计算代价即h(x)+g(x)
    if(expense > bound):return expense  #如果代价大于界限，则返回该代价
    if(node == end_state):  #如果找到了相匹配的目标状态，则返回0，表示成功找到
        return 0
    index = node.index(0)   #获取0在数组中的位置
    x = index % 4
    y = index // 4
    moves = []  #创建moves数组，存储偏移量
    if x > 0 and index - 1 >= 0 : moves.append(-1)    # 左移
    if x < 3 and index + 1 < 16 : moves.append(+1)    # 右移
    if y > 0 and index - 4 >= 0 : moves.append(-4)    # 上移
    if y < 3 and index + 4 < 16 : moves.append(+4)    # 下移
    res = 1000          #定义res，用它来找到子节点中的最小f(x)
    for m in moves:
        #生成子节点
        temp = list(node)   #将tuple转换为list，方便修改生成子状态
        swap(temp,index,index+m)    #进行交换
        s = tuple(temp)     #将list转换为tuple，实现格式对齐
        if(s in close):continue #进行环检测
        else :close.add(s)
        path.append(s)   #将生成的子节点加入path路径中
        ans = dfs(bound,g+1)     #递归搜索
        if(ans == 0):return 0   #如果返回值为零则表示已经找到了答案，这时候便可以返回0
        if(ans < res): res = ans     #如果没有找到答案，则更新res值，取较小的一个
        path.pop()        #删去最后一个节点，进行回溯
        close.remove(s)    #同理删去close表中的新生成的节点，以便回溯
    return res

def IDA_Star(start):
    bound = calculate_h(start)  #以初始节点的f(x)值作为初始bound
    path.append(start)
    close.add(start)
    while(True):
        #假定存在答案，进行循环搜索
        ans = dfs(bound, 0)
        if(ans == 0):return [bound,path]    #返回边界和路径
        bound = ans     #根据搜索到的子节点的f(x)的最小值更新bound值，进行下一轮的搜索

if __name__ == '__main__':
    start = loadtxt('test7.txt',dtype = int, delimiter = ',')
    start_state = tuple(start.flatten())
    close = set()
    tic = timer()
    combine = IDA_Star(start_state)
    toc = timer()
    res = combine[1]
    s1 = "We tried "+str(len(res)-1)+" times\n"
    line = "---------------\n"
    s2 = "The search time is "+str(toc-tic)+" seconds!\n"
    
    with open('IDA_result7.txt','w') as f:
        '''将输入打印到结果文件中'''
        for i in range(len(res)):
            r = np.array(list(res[i])).reshape(4,4)
            f.writelines(' '+str(r)[1:-1])
            if(i>=1):
                f.writelines("   step "+str(i))
            f.writelines('\n'+line)
        f.writelines(s1)
        f.writelines(s2)


