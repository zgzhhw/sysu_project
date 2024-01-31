import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from timeit import default_timer as timer
import math

label_dict = {"joy": 4,"disgust": 2,"anger": 1 ,"fear": 3,"sad": 5 ,"surprise":6}

def distance(x1, x2):
    """计算两个向量的欧氏距离"""
    x1 = np.array(x1)
    x2 = np.array(x2)
    return np.sqrt(np.sum((x1 - x2)**2))

def read_file(filename):
    """读取并分离输入文件中的信息"""
    texts = []  #存储测试文本信息
    labels = [] #存储测试用的标签
    with open(filename, 'r') as f:
        for line in f:
            s = line.strip().split(' ')
            if s[0] == 'documentId':
                continue
            text = s[3]
            for c in s[4:]:
                text += ' ' + c
            label = label_dict[s[2]]
            texts.append(text)
            labels.append(label)
    return texts, labels

def knn_dis(train_set, train_labels, test_set, k):
    n_train = train_set.shape[0]    #获取训练集的行的数量
    n_test = test_set.shape[0]      #获取测试集的行的数量
    dis = np.zeros((n_test, n_train))   #建立全为零的二维数组，存储向量的距离
    test = test_set.toarray()   
    train = train_set.toarray()     #转换成列表，将矩阵square化，便可以计算其向量距离
    for i in range(n_test):
        for j in range(n_train):
            dis[i][j] = distance(test[i], train[j])
    pred_labels = np.zeros(n_test, dtype=int)   #存储预测值
    for i in range(n_test):
        indices = np.argsort(dis[i])[:k]    #进行排序，获取前k个距离最短的元素的索引
        k_labels = train_labels[indices]    #根据索引获取label，存储再k_labels中
        pred_label = np.argmax(np.bincount(k_labels))   #调用np库计算众数
        pred_labels[i] = pred_label #将获得的众数预测值赋值给pred_labels的第i个元素
    return pred_labels

def knn_cos(train_set, train_labels, test_set, k=5):
    """k-NN分类算法"""
    n_train = train_set.shape[0]
    n_test = test_set.shape[0]  #获取两个测试集的行的数量
    sim = cosine_similarity(test_set, train_set)    #调用库函数计算余弦相似度
    pred_labels = np.zeros(n_test, dtype=int)   #创建一个一维数组存储结果
    for i in range(n_test):
        indices = np.argsort(sim[i])[-k:]   #反向排序，这点与欧氏距离不相同，这个是相似度越大越好
        k_labels = train_labels[indices]    #将相对应的标签存储到k_labels中
        k_sim = sim[i][indices]     #将相对应的训练集样本存储到k_sim中
        max_count = 0
        pred_label = 0
        for label in set(k_labels):
            count = sum(k_labels == label)  #计算邻居中标签与当前标签相同的个数
            weight = sum(k_sim[k_labels == label])  #计算当前标签的相似度权重
            if count > max_count or (count == max_count and weight > max_weight):
            #如果count大于max_count或者在两者相同的情况下权重weight大于max_weight则更新
                max_count = count
                max_weight = weight
                pred_label = label
        pred_labels[i] = pred_label
    return pred_labels

def calculate_accuracy(predict, test):
    res = [0.0,0.0,0.0,0.0,0.0,0.0]
    length = [0,0,0,0,0,0]
    count = 0
    for i in range(len(test)):
        if(predict[i] == test[i]):
            res[test[i]-1] += 1.0
            count += 1

        length[test[i]-1] += 1
    for i in range(6):
        res[i] /= length[i]
    return res,count


train_texts, train_labels = read_file('train.txt')  #通过读文件获取测试集和标签集
test_texts, test_labels = read_file('test.txt') 

train_labels = np.array(train_labels)   #将标签集合转换为np数组，才能作为参数传入knn函数中

tfidf = TfidfVectorizer()   #创建tfidf类    
train_set = tfidf.fit_transform(train_texts)    #前者调用fit_transform函数固定化匹配模板
test_set = tfidf.transform(test_texts)  #后者直接调用transform函数直接套用前面的模板，达到对齐的效果

tic = timer()
pred_labels = knn_dis(train_set, train_labels, test_set, 16)   #调用knn函数，返回预测列表
toc = timer()
accuracy = calculate_accuracy(pred_labels, test_labels)   #统计正确率
for i in range(6):
    print(f'The accuracy of the {i+1}th mood is : {accuracy[0][i]:.4f}')
print(f'The total accuracy: {accuracy[1]/(len(test_labels)):.4f}')
print(f"Your cost_time is {(toc-tic):.4f} seconds!")

