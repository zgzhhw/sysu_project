import pandas as pd
import numpy as np
import nltk
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import LabelEncoder
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from timeit import default_timer as timer

# 1. 加载数据和预处理
def read_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            fields = line.split('\t')
            data.append(fields)
    return data

train_data = read_file('train_40.tsv')
test_data = read_file('dev_40.tsv')

train_df = pd.DataFrame(train_data[1:], columns=train_data[0])
test_df = pd.DataFrame(test_data[1:], columns=test_data[0])

train_df.dropna(inplace=True)
test_df.dropna(inplace=True)

stopwords_set = set(stopwords.words('english'))  # 创建停用词列表，过滤掉经常出现但是携带很少信息的词

# Tokenize函数，用于将文本分词并去除停用词
def tokenize(text):
    tokens = word_tokenize(text)
    tokens = [token.lower() for token in tokens if token.isalpha() and token.lower() not in stopwords_set] #转换成小写并去除停用词与标点符号
    return tokens

# 将tokenize函数应用于question和sentence列，进行分词操作，并将结果储存回对应的列中
train_df['question'] = train_df['question'].apply(tokenize)
train_df['sentence'] = train_df['sentence'].apply(tokenize)
test_df['question'] = test_df['question'].apply(tokenize)
test_df['sentence'] = test_df['sentence'].apply(tokenize)

# 标签编码
label_encoder = LabelEncoder()
train_df['label'] = label_encoder.fit_transform(train_df['label']) #将label中的每一个类别映射为一个整数编码
test_df['label'] = label_encoder.transform(test_df['label'])    #对应一致，方便操作

# 2. 构建词汇表
word_index = {}
index = 1
for _, row in train_df.iterrows():
    for token in row['question'] + row['sentence']:
        if token not in word_index:
            word_index[token] = index   # 为问题和句子中的所有单词分配唯一的索引
            index += 1

vocab_size = len(word_index) + 1

# 加载预训练词向量
word_vectors = {}
with open('glove.6B.50d.txt', 'r', encoding='utf-8') as file:
    for line in file:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], dtype='float32')
        word_vectors[word] = vector

embedding_dim = 50
embedding_matrix = np.zeros((vocab_size, embedding_dim))
for word, i in word_index.items():
    vector = word_vectors.get(word)
    if vector is not None:
        embedding_matrix[i] = vector    # 将索引与预训练词向量一一对应

# 3. 构建Dataset和DataLoader
class TextDataset(Dataset):
    def __init__(self, df, word_index, max_length):
        self.questions = df['question']
        self.sentences = df['sentence']
        self.labels = df['label']
        self.word_index = word_index
        self.max_length = max_length

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        question = self.questions.iloc[index]
        sentence = self.sentences.iloc[index]
        label = self.labels.iloc[index]
        label = torch.tensor(int(label))  

        # 将问题和句子进行索引化操作，将问题和句子中的每一个单词转换为词汇表中对应的索引
        question_indices = [self.word_index[word] for word in question if word in self.word_index]
        sentence_indices = [self.word_index[word] for word in sentence if word in self.word_index]

        # 截断操作，相当于数据对齐
        question_indices = question_indices[:self.max_length]
        sentence_indices = sentence_indices[:self.max_length]

        # 填充操作
        padded_question = np.pad(question_indices, (0, self.max_length - len(question_indices)), mode='constant')
        padded_sentence = np.pad(sentence_indices, (0, self.max_length - len(sentence_indices)), mode='constant')

        # 转换为张量
        padded_question = torch.tensor(padded_question, dtype=torch.long)
        padded_sentence = torch.tensor(padded_sentence, dtype=torch.long)

        return padded_question, padded_sentence, label


max_length = max(
    train_df['question'].apply(len).max(),
    train_df['sentence'].apply(len).max(),
    test_df['question'].apply(len).max(),
    test_df['sentence'].apply(len).max()
)

train_dataset = TextDataset(train_df, word_index, max_length)
test_dataset = TextDataset(test_df, word_index, max_length)

train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)

# 4. 构建模型
class LSTMModel(nn.Module):
    def __init__(self, embedding_matrix, hidden_size, num_classes):
        super(LSTMModel, self).__init__()
        self.embedding = nn.Embedding.from_pretrained(torch.FloatTensor(embedding_matrix)) # 使用预训练的词嵌入矩阵进行初始化
        self.lstm = nn.LSTM(embedding_dim, hidden_size, batch_first=True)   # 构建LSTM模型，定义输入层，隐藏层
        self.fc = nn.Linear(hidden_size, num_classes)   # 定义全连接层， 输出的种类为2

    def forward(self, x_question, x_sentence):
        """前向传播方法"""
        embedded_question = self.embedding(x_question) # 将输入的问题序列和句子序列转换为对应的词嵌入表示
        embedded_sentence = self.embedding(x_sentence)
        _, (question_hn, _) = self.lstm(embedded_question)  # 返回最后一个时间步的输出
        _, (sentence_hn, _) = self.lstm(embedded_sentence)
        merged = question_hn[-1] + sentence_hn[-1]  # 将最后一个时间步的输出进行合并
        output = self.fc(merged)    # 进行分类操作，得到模型的输出
        return output

hidden_size = 64
num_classes = 2

model = LSTMModel(embedding_matrix, hidden_size, num_classes) # 创建模型

# 5. 训练模型
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)    # 使用优化器

model.to(device)

num_epochs = 10
best_loss = float('inf')
patience = 3
counter = 0
for epoch in range(num_epochs):
    tic = timer()
    model.train()
    total_loss = 0
    total_correct = 0
    for batch in train_loader: # 从训练集中取出一个批次的数据
        x_question, x_sentence, labels = batch
        x_question = x_question.to(device)
        x_sentence = x_sentence.to(device)
        labels = labels.to(device)

        optimizer.zero_grad() # 将梯度归零，清楚之前的梯度信息
        output = model(x_question, x_sentence)  # 分类操作
        loss = criterion(output, labels)    # 计算loss
        loss.backward() # 反向传播，计算参数的梯度
        optimizer.step()    # 使用优化器更新模型的参数

        total_loss += loss.item()
        total_correct += (output.argmax(1) == labels).sum().item()

    # 计算每一个批次的损失与预测正确率
    train_loss = total_loss / len(train_dataset)
    train_acc = total_correct / len(train_dataset)

    model.eval()    # 将模型设置为评估模式
    total_correct = 0
    total_loss = 0
    with torch.no_grad():   # 禁用梯度计算以加快评估过程
        for batch in test_loader:
            x_question, x_sentence, labels = batch
            x_question = x_question.to(device)
            x_sentence = x_sentence.to(device)
            labels = labels.to(device)
            output = model(x_question, x_sentence)
            loss = criterion(output, labels)    # 计算loss
            total_loss += loss.item()
            total_correct += (output.argmax(1) == labels).sum().item()

    test_acc = total_correct / len(test_dataset)
    test_loss = total_loss / len(test_dataset)

    toc = timer()
    print("Epoch {}/{} - Train Loss: {:.4f} - Train Acc: {:.4f} - Test Acc: {:.4f} - Test Loss: {:.4f} - Spent time: {:.4f}".format(epoch+1, num_epochs, train_loss, train_acc, test_acc, test_loss, toc - tic))
    if test_loss < best_loss:
        best_loss = test_loss
        counter = 0
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping.")
            break

# 6. 结果输出
model.eval()
total_correct = 0
with torch.no_grad():
    for batch in test_loader:
        x_question, x_sentence, labels = batch
        x_question = x_question.to(device)
        x_sentence = x_sentence.to(device)
        labels = labels.to(device)
        output = model(x_question, x_sentence)
        total_correct += (output.argmax(1) == labels).sum().item()

test_acc = total_correct / len(test_dataset)
print("Accuracy:", test_acc)
