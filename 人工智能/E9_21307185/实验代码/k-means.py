import numpy as np
import matplotlib.pyplot as plt
import random

def distance(x1, x2):
    """计算两个向量的欧氏距离"""
    x1 = np.array(x1)
    x2 = np.array(x2)
    return np.sqrt(np.sum((x1 - x2)**2))

def read_file(filename):
    """读取并分离输入文件中的信息"""
    data = np.loadtxt(filename, delimiter=',',skiprows=1, dtype=float)  # 跳过第一行读取，类型为float
    return data

def classify(data, center, k):
    """分类函数,将数据集合进行分类"""
    dis = np.zeros((len(data), len(center)))  #初始化距离数组
    for i in range(len(data)):
        for j in range(len(center)):
            dis[i][j] = np.linalg.norm(data[i] - center[j]) #求出数据样本距离给定的数据中心的距离
    min_dis = np.argmin(dis, axis=1)    #返回距离最小索引的列表
    cluster = [[] for i in range(k)]
    for i in range(len(min_dis)):
        cluster[min_dis[i]].append(data[i]) #对于每一个样本中心，根据前面求得的min_dis列表的值进行归类
    new_center = []
    for i in range(k):
        new_center.append(np.mean(cluster[i], axis=0).tolist()) #分类之后再根据得到的分类结果求出每个数据集合的中心
    return cluster, new_center

def init_center(data,k):
    """随机选取样本初始中心"""
    return random.sample(data.tolist(),k)

def init_center_plus(data,k):
    """根据kmeans++选择初始样本中心"""
    centers = []
    centers.append(random.sample(data.tolist(),1)[0])   #随机选取一个点作为初始样本中心
    for cnt in range(1,k):  #选取剩下的样本中心
        dist = []
        for i in range(len(data)):
            dis = 0
            for j in range(len(center)):
                dis += distance(data[i],center[j])  #求出每个样本点与现有的样本中心的距离之和
            dist.append(dis)
        new_item = None
        while True:
            new_item = random.choices(data.tolist(),dist,k=1)[0]    #根绝dist数组设置权重，生成权重数组，选择新的中心
            if(new_item not in centers):break   #检查新生成的样本中心是否再原来已有的样本中心中，如果在则继续
        centers.append(new_item)
    return centers

def k_means(center,data,k,mistake=0.00001, max_iters=100):  #设置误差值和最大循环次数
    """k_means核心算法,求解聚类"""
    for i in range(max_iters):  #设置最大循环次数，防止过度循环而浪费时间和资源
        cluster,new_center = classify(data, center, k)
        distance = np.linalg.norm(np.array(new_center) - np.array(center))
        if distance < mistake:  #如果在误差值以内则退出，成功分类
            break
        center = new_center
    return cluster, new_center  #返回聚类和当前的聚类中心

def calculate_sse(cluster,center,k):
    """计算在不同的k值下的SSE值"""
    sum = 0.0
    for i in range(k):
        for j in range(len(cluster)):
            for k in range(len(cluster[j])):
                sum += distance(cluster[j][k],center[j])**2
    return sum

data = read_file('kmeans_data.csv')
sse = []
for k in range(1,9):    #循环测试多个k值
    init_cent = init_center(data, k)
    cluster,center = k_means(init_cent,data, k)
    sse.append(calculate_sse(cluster, center, k))

plt.plot(range(1, 9), sse)
plt.xlabel('Number of clusters')
plt.ylabel('SSE')
plt.show()  #将SSE值随k的变化的折线图绘制出来

init_cent = init_center(data, 3)    #根据折线图可知 k = 3 处为最佳
cluster,center = k_means(init_cent,data, 3)
colors = ['r','b','g','k','c','m','y','w']  #设置颜色列表，标记成不同颜色
for i in range(len(cluster)):
    plt.scatter([x[0] for x in cluster[i]], [x[1] for x in cluster[i]], c=colors[i%len(colors)],cmap = 'viridis')
    #为每个聚类赋予不同的颜色标记
plt.show()  #将最终的分类结果展示出来

