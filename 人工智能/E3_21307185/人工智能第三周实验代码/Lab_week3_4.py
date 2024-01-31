import numpy
import copy
class Predicate:
    """表示谓词的类"""
    def __init__(self,name='',arr=[],row=0,col='a',flag=True):
        self.name=name      #谓词名
        self.arr=arr        #存储变量或实例
        self.row=row        #谓词所在的行
        self.col=col        #谓词在子句中的位置
        self.flag=flag      #正或负文字
        self.function=[]    #存储谓词中函数的列表

class TreeNode:
    def __init__(self,val,left = 0,right = 0,replace = {},r_map = {},parent = [],parent_col = []):
        self.val=val                #存储子句
        self.left=left              #左儿子
        self.right=right            #右儿子
        self.replace=replace        #变元替换的实例
        self.r_map=r_map            #函数映射
        self.parent=parent          #由哪两句归结而来
        self.parent_col=parent_col  #如果为0则表示一行中只有一个谓词
        self.wasted = False         #表示是否用于归结

def read_line(s,row):
    remain = 0
    stack_predicate = []    #存储谓词的栈
    stack_function = []     #存储函数的栈
    while (' ' in s):s=s.replace(' ',"")
    if(s[0]=='('):s = s[1:-1]
    col = -1
    res=[]
    p=0
    while (p < len(s)):
        if(s[p] == '('):    #如果遇到左括号则将remain + 1并continue
            remain += 1
            p += 1
            continue    
        if(s[p] == ')'):    #如果遇到右括号则将remain - 1并continue
            remain -= 1
            p += 1
            continue
        if(remain==0 and s[p]==','):    #当remain == 0表示在谓词层面，如果遇到逗号，则表示谓词的分割，将谓词加入子句
            p += 1
            res.append(stack_predicate[-1])
            continue
        if(remain == 1 and s[p] == ','): #如果remain==1，则表示在变量层面，此时直接继续
            p+=1
            continue
        if(remain == 0):    #谓词名层面
            temp = Predicate()
            col += 1
            if(s[p] == '~'):
                temp.flag = False
                p += 1
            j = p
            while (s[j]!='('):  #遍历到左括号获取谓词名
                j+=1
            temp.name = s[p:j]
            temp.row = row
            temp.col = chr(ord('a')+col)
            temp.arr=[]         #初始化谓词变量列表
            p=j-1
            stack_predicate.append(temp)
        if(remain == 1): #谓词变元层面
            j = p
            flag = True
            temp = stack_predicate[-1]  #获取谓词栈中栈顶元素
            while(s[j]!=')'):
                if(s[j] == '('):
                    flag = False
                    break
                j+=1
            if(flag): #表示变元中没有函数
                cur = s[p:j]
                array = cur.split(',')
                for a in array:
                    temp.arr.append(a)
                    temp.function.append({})
                p=j-1
            else:   #表示变元中有函数
                k = p
                while(s[k]!=',' and s[k]!=')'):k+=1
                word = s[p:k]
                if('(' in word):
                    k = p
                    while(s[k]!='('):k+=1
                    fun = s[p:k]    #获取函数名
                    temp.arr.append(fun)
                    temp.function.append({})
                    stack_function.append(fun)
                    p = k-1         
                else :
                    temp.arr.append(word)
                    temp.function.append({})
                    p = k-1
        if(remain >= 2):    #函数层面
            temp=stack_predicate[-1]
            j = p
            while(s[j]!=')'):j+=1
            word = s[p:j]
            if('(' in word):
                fun_pre = stack_function[-1]    #获取之前的函数名，方便使用映射
                k = p
                while(s[k]!='('):k+=1
                fun = s[p:k]
                temp.function[-1][fun_pre]=fun
                stack_function.append(fun)
                p = k-1
            else :
                fun = stack_function[-1]
                temp.function[-1][fun]=word
                p = j-1
        p+=1
    res.append(stack_predicate[-1])
    return res

def reverse_function_map(function):
    """反转映射函数字典的键值对"""  #方便进行归结匹配
    func = {v:k for k,v in function.items()}
    return func

def create_list():
    """将文件输入转化为列表存储"""
    f=open('test4.txt','r')
    count_row=1     #计算行数
    store=[]
    for line in f:
        line=line.strip()
        s=line
        array = read_line(s,count_row)
        for i in range(len(array)):
            for j in range(len(array[i].arr)):
                x = array[i].arr[j]
                while (x in array[i].function[j]):x = array[i].function[j][x]
                array[i].function[j]=reverse_function_map(array[i].function[j])
                array[i].arr[j] = x
        store.append(array)
        count_row += 1
    return convert_TreeNode_list(store)

def convert_TreeNode_list(store):
    """将每个字句存储在树的节点中,并将所有树的节点存放到一个列表中并返回"""
    TreeNode_store=[]
    for i in range(len(store)):
        line = store[i]
        root = TreeNode(line)
        TreeNode_store.append(root)
    return TreeNode_store

def is_same_predicate(node_a,node_b):
    """判断两个谓词是否相同"""
    if(node_a.name != node_b or len(node_a.arr) != len(node_b.arr) or node_a.flag != node_b.flag):return False
    for i in range(len(node_a.arr)):
        if(node_a.arr[i]!=node_b.arr[i]) : return False
    return True

def is_in_line(node,line):
    """判断一个谓词是否在字句集中"""
    for l in line:
        if(is_same_predicate(node,l)):return True
    return False

def construct(left,right,replace,index,cur_len):
    """创建归结后的列表,并返回节点"""
    if(len(right)):
        for i in range(len(right)):
            if(not is_in_line(right[i],left)):
                left.insert(index,right[i])
                index+=1
    for i in range(len(left)):
        left[i].col = chr(ord('a')+i)
        left[i].row = cur_len           #更新行和列
        for j in range(len(left[i].arr)):
            if(left[i].arr[j] in replace):  #利用 replace 字典替换变量为实例
                left[i].arr[j] = replace[left[i].arr[j]]
    return left


def bfs(root):
    """通过层序遍历即广度优先搜索生成匹配序列"""
    store = []
    store.append(root)
    res = []
    while(len(store)):
        temp = store[0]     #获取队首元素
        store.pop(0)        #弹出队首元素
        if (temp.left != 0):store.append(temp.left)
        if (temp.right != 0):store.append(temp.right)
        res = res + temp.parent             #这里可能出现一个节点是多个节点的父亲，后面会进行去重操作
    return res
        
def match_line(root1,root2,store_len):
    """匹配子句集,按逐行方式匹配"""
    line1 = root1.val
    line2 = root2.val
    for k in range(len(line1)):
        for j in range(len(line2)):
            node1=line1[k]
            node2=line2[j]
            replace={}
            r_map = {}
            if(node1.name != node2.name or len(node1.arr) != len(node2.arr) or node1.flag==node2.flag):continue
            flag = True
            for i in range(len(node1.arr)):
                if (len(node1.arr[i])<len(node2.arr[i]) and len(node1.arr[i]) == 1 and node1.arr[i] not in node1.function[i]):
                    replace[node1.arr[i]]=node2.arr[i]
                elif (len(node1.arr[i])>len(node2.arr[i]) and len(node2.arr[i]) == 1 and node2.arr[i] not in node2.function[i]):
                    replace[node2.arr[i]]=node1.arr[i]
                else :
                    if(node1.arr[i]!=node2.arr[i] and len(node1.arr[i])>1):
                        flag = False
                    elif (node1.arr[i]!=node2.arr[i] and len(node1.arr)==1):
                        #如果有函数的情况则判断是否可以匹配
                        if(node1.arr[i] in node1.function[i] and node2.arr[i] not in node2.function[i]):
                            r = node1.arr[i]
                            if(r in node1.function[i]):replace[node2.arr[i]] = r 
                            while(r in node1.function[i]):
                                r_map[r] = node1.function[i][r]
                                r = node1.function[i][r]
                        elif(node2.arr[i] in node2.function[i] and node1.arr[i] not in node1.function[i]):
                            r = node2.arr[i]
                            if(r in node2.function[i]):replace[node1.arr[i]] = r 
                            while (r in node2.function[i]):
                                r_map[r] = node2.function[i][r]
                                r = node2.function[i][r]
            if(flag):
                line1_temp=copy.deepcopy(line1)
                line2_temp=copy.deepcopy(line2) #进行深拷贝，防止对原列表中的元素进行修改
                index1=line1.index(node1)
                index2=line2.index(node2)
                line1_temp.pop(index1)
                line2_temp.pop(index2)
                root_val = construct(line1_temp,line2_temp,replace,index1,store_len+1)
                col1=0
                col2=0                          #为了避免一个子句中只有一个谓词而错误加上abc等
                if(len(line1)>1):col1=index1+1
                if(len(line2)>1):col2=index2+1
                root = TreeNode(root_val,root1,root2,replace,r_map,[node1.row,node2.row],[col1,col2])
                #创建根节点
                root.left = root1
                root.right = root2
                if(not in_store(root,store)):
                    store.append(root)      #判断新生成的root_node在不在store中，如果在的话则去掉，否则加入到末尾
                return True
    return False 

def remove_trash(store,bfs_list,initial_len):
    """将没有参与匹配的字句进行标记和对子句列表进行重规划行"""
    bfs_list.sort()
    map = {}        #表示归结所用到的子句行在输出时需要减去的行数
    count =0
    for i in range(len(store)):
        if(i+1 <= initial_len):
            map[i+1] = 0
        elif(i+1 in bfs_list):
            map[i+1] = count
        else: 
            count += 1
            store[i].wasted = True      #不在遍历序列中，则舍弃，在输出的时候不显示
    return map

def in_store(node,store):
    """判断一个树节点是否在store列表中"""
    flag = False
    for s in store:
        if(len(node.val) != len(s.val) ):continue
        for i in range(len(node.val)):
            count = 0
            if(len(node.val[i].arr) != len(s.val[i].arr)):break
            for j in range(len(node.val[i].arr)):
                if(node.val[i].arr[j] == s.val[i].arr[j]):
                    count+=1
            if(node.val[i].name == s.val[i].name and node.val[i].flag == s.val[i].flag and count == len(node.val[i].arr)):
                flag=True
    return flag

def create_root(store):
    """将store中的树节点依次匹配,并添加到store的末尾,最终生成一个空列表树节点"""
    length=len(store)
    i=0
    while(i<length-1):
        """注意:这里如果使用for i in range(len(store))的话,不会实时更新,导致有很多子句没有被遍历到"""
        j=i+1
        while(j<length):
            match_line(store[i],store[j],len(store))
            if(len(store[-1].val)==0):#如果最后生成了一个空列表，则返回
                return store[-1]
            j=j+1
        store[i].visited=True
        i=i+1
        length=len(store)
    return store[-1]

def get_parent_list(root,map,size):
    """获取双亲节点,便于答案的生成"""
    store = []  #队列，进行层序遍历
    store.append(root)
    array = []
    while(len(store)):
        temp = store[0]
        store.pop(0)
        if(temp.left != 0):store.append(temp.left)
        if(temp.right != 0):store.append(temp.right)
        if(len(temp.parent)==0):continue
        if(temp.parent_col[0]):s = str(temp.parent[0]-map[temp.parent[0]])+chr(temp.parent_col[0]-1+ord('a'))
        else :s=str(temp.parent[0]-map[temp.parent[0]])
        s += ","
        if(temp.parent_col[1]):s += str(temp.parent[1]-map[temp.parent[1]])+chr(temp.parent_col[1]-1+ord('a'))
        else :s += str(temp.parent[1]-map[temp.parent[1]])
        cur = 0
        if(len(temp.val)==0):cur = size
        else: cur = temp.val[0].row
        node = [cur,s]
        flag = True
        for arr in array:
            if(s==arr[1]):flag=False
        if(flag):array.append(node)  #列表中的第一个元素表示生成的新的归结子句在第几行，第二个元素表示由哪几个谓词归结得来
    array.sort()            #按照生成行的顺序进行排序
    return array

def flush_store(store,map):
    """刷新store列表,将用到的归结子句的行进行更改"""
    for i in range(len(store)):
        line = store[i].val
        for j in range(len(line)):
            if(line[j].row in map):
                line[j].row -= map[line[j].row]

def print_list(store):
    """打印带结构体的列表"""
    for i in range(len(store)):print_line(store[i].val)

def print_line(line):
    """打印子句"""
    flag = len(line)>1
    if(flag):print("(",end="")
    for i in range(len(line)):
        print_predicate(line[i])
        if(i<len(line)-1):print(",",end="")
    if(flag):print(")",end="")
    print()

def print_predicate(node):
    """打印谓词"""
    if(node.flag==False):print("~",end="")
    print(node.name,"(",end="",sep="")
    for i in range(len(node.arr)):
        print_function(node.arr[i], node.function[i])
        if( i < len(node.arr)-1):
            print(",",end="")
    print(")",end="")

def print_function(fun,func):
    """打印函数"""
    x = fun 
    while(x in func):x = func[x]
    map = reverse_function_map(func)
    fun = x
    print(fun,end="")
    left = 0
    while(fun in map):
        print('(',map[fun],end="",sep="")
        fun = map[fun]
        left += 1
    while(left):
        print(')',end="")
        left -= 1

def print_answer(store,array,map):
    """打印答案"""
    for k in range(len(array)):
        arr = array[k]
        print("R[",arr[1],"]",end="",sep="")
        node = store[arr[0]-1]
        if(node.replace):
            for k,v in node.replace.items():
                print("(",k,'=',sep="",end="")
                if(v in node.r_map):
                    print_function(v, node.r_map)
                else: print(v,end="")
                print(")",end="")
        print(" = ",end="")
        if(len(node.val)==0):print("[]")
        else: print_line(node.val)

"""主函数"""
store=create_list()
print_list(store)
size=len(store)
root = create_root(store)
map = remove_trash(store, bfs(root), size)
s = get_parent_list(root, map, len(store))
flush_store(store, map)
print_answer(store,s,map)
