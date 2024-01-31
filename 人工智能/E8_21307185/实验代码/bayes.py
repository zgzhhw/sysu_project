import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from timeit import default_timer as timer
import math
from collections import defaultdict

label_dict = {"joy": 4,"disgust": 2,"anger": 1 ,"fear": 3,"sad": 5 ,"surprise":6}
lamda = 100

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

def calculate_prior(train_labels):
    """计算每个类出现的先验概率"""
    class_count = np.bincount(train_labels)[1:]  # 统计每个类别的样本数量
    class_prior = class_count / len(train_labels)  # 计算每个类别的先验概率
    return class_prior



def calculate_case(train_labels,train_texts,vocabulary):
    """计算每个文本特征出现在各自情感类的条件概率"""
    class_probs = defaultdict(dict)  # 存储每个类别下每个特征的条件概率
    num_features = train_set.shape[1]
    word_count = {1: defaultdict(int), 2: defaultdict(int), 3: defaultdict(int),
                  4: defaultdict(int), 5: defaultdict(int), 6: defaultdict(int)}
    class_count = {1:0,2:0,3:0,4:0,5:0,6:0}
    for i in range(len(train_labels)):
        label = train_labels[i]
        s = train_texts[i].split(' ')
        for word in s:
            word_count[label][vocabulary.get(word)] += 1
        class_count[label] += len(s)
    for c in range(1,7):
        # 统计训练集中属于类别 c 的文本数目
        num_docs_in_class = class_count[c]
        for j in range(num_features):
            # 统计属于类别 c 的文本中特征 j 出现的次数
            count = word_count[c][j]
            # 计算条件概率 P(x_j|c_i)
            class_probs[c][j] = (count + lamda) / (num_docs_in_class + lamda * num_docs_in_class)   #平滑处理
    return class_probs

def predict(test_texts,test_labels,vocabulary,class_prior,class_probs):
    """预测函数,根据测试集的样本预测并计算正确率"""
    test_probs = test_set.toarray()
    count = [0,0,0,0,0,0]   
    size = [0,0,0,0,0,0]
    accuracy = [0.0,0.0,0.0,0.0,0.0,0.0]    #统计每一个情感类的预测正确率
    cnt = 0
    for k in range(len(test_texts)):
        t = test_texts[k]
        words = t.split(' ')
        probs = []     #存储每个类的后验概率，选择最大的返回
        for c in range(1,7):
            sum = 0.0   #存储语句中单词的后验概率之和
            for word in words:
                if(word not in vocabulary):continue #如果在训练集中的单词未在测试集中出现，则跳过
                index = vocabulary.get(word)
                sum += class_prior[c-1] * class_probs[c][index]  #计算后验概率，分母一致就不用管了
            probs.append(sum)
        res = np.argmax(probs) + 1  #返回最大概率的下标，不要忘了加一表示相应的类
        if(res == test_labels[k]):
            count[res-1] += 1
            cnt += 1
        size[test_labels[k] - 1] += 1
    for i in range(6):
        accuracy[i] = count[i] / size[i]
        print(f'The {i+1}th class Accuracy: {accuracy[i]:.4f}')

    print(f'The total Accuracy: {cnt/len(test_texts):.4f}')

if __name__ == '__main__':
    """主函数"""
    train_texts, train_labels = read_file('train.txt')  #通过读文件获取测试集和标签集
    test_texts, test_labels = read_file('test.txt') 
    train_labels = np.array(train_labels)   #将标签集合转换为np数组，才能作为参数传入knn函数中

    tfidf = TfidfVectorizer()   #创建tfidf类    
    train_set = tfidf.fit_transform(train_texts)#前者调用fit_transform函数固定化匹配模板
    vocabulary = tfidf.vocabulary_    #生成反映射到索引的单词的字典
    test_set = tfidf.transform(test_texts)  #后者直接调用transform函数直接套用前面的模板，达到对齐的效果

    probs_prior = calculate_prior(train_labels) #计算先验概率
    probs_case = calculate_case(train_labels,train_texts,vocabulary)    #计算条件概率
    predict(test_texts, test_labels, vocabulary, probs_prior, probs_case)   #根据给定的文本输入进行预测，并打印预测正确率

