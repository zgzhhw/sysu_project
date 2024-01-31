import pandas as pd
import numpy as np
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Embedding, LSTM, Dense, Input
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf

# 1. 加载训练集和测试集数据
def read_file(filename):
    data = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # 去除行尾的换行符
            fields = line.split('\t')  # 使用制表符('\t')分割字段
            data.append(fields)
    return data

train_data = read_file('train_40.tsv')
test_data = read_file('dev_40.tsv')

# 将原始的训练数据和测试数据转换为Pandas DataFrame的形式，以便进行后续的数据处理和分析
train_df = pd.DataFrame(train_data[1:], columns=train_data[0])
test_df = pd.DataFrame(test_data[1:], columns=test_data[0])

# 清除训练集中的空值
train_df.dropna(inplace=True)
# 清除测试集中的空值
test_df.dropna(inplace=True)

# 2. 数据预处理
# 下载punkt数据文件，利用其中的分词规则进行分词操作
nltk.download('punkt') 
# 将训练集中的 'question' 列中的每个句子应用 word_tokenize 函数进行分词处理，分词后的结果会覆盖原始的句子内容
train_df['question'] = train_df['question'].apply(nltk.word_tokenize)
# 下面的分词操作同理
train_df['sentence'] = train_df['sentence'].apply(nltk.word_tokenize)
test_df['question'] = test_df['question'].apply(nltk.word_tokenize)
test_df['sentence'] = test_df['sentence'].apply(nltk.word_tokenize)

# 3. 词嵌入（word embedding）
tokenizer = Tokenizer()
# 调用fit_on_texts方法，将训练集中的问题和句子拼接起来作为输入。
# 根据输入文本构建词汇表，统计每个单词出现的频率，并为每个单词分配一个唯一的整数索引
tokenizer.fit_on_texts(train_df['question'] + train_df['sentence'])
# 计算词汇表的长度，由于索引从1开始，因此要+1
vocab_size = len(tokenizer.word_index) + 1

# 加载预训练词向量
word_vectors = {}
with open('glove.6B.50d.txt', 'r', encoding='utf-8') as file:
    for line in file:
        values = line.split()
        word = values[0]
        vector = np.asarray(values[1:], dtype='float32')
        word_vectors[word] = vector

# 创建词嵌入矩阵
embedding_dim = 50 # 与预训练的向量维度匹配
embedding_matrix = np.zeros((vocab_size, embedding_dim))
for word, i in tokenizer.word_index.items():
    vector = word_vectors.get(word) #从预训练向量中获取word的向量
    if vector is not None:
        embedding_matrix[i] = vector    #如果非空，则将词向量置于embedding_matrix矩阵的对应位置

# 4. 数据对齐（pad_sequence）

# 计算出所有句子中的最大长度，作为padding的值，用于长度对齐
max_length = max(train_df['question'].apply(len).max(), train_df['sentence'].apply(len).max(),
                test_df['question'].apply(len).max(), test_df['sentence'].apply(len).max())
# 将训练集的问题（question）文本转换为对应的序列（由单词索引组成的列表）
X_train_question = tokenizer.texts_to_sequences(train_df['question'])
# 将训练集的问题序列进行padding操作，长度不足的部分用0进行填充
X_train_question = pad_sequences(X_train_question, maxlen=max_length, padding='post')
# 对语句的操作类似
X_train_sentence = tokenizer.texts_to_sequences(train_df['sentence'])
X_train_sentence = pad_sequences(X_train_sentence, maxlen=max_length, padding='post')
# 对训练集的标签进行编码，将其转换为数值形式
label_encoder = LabelEncoder()
y_train = label_encoder.fit_transform(train_df['label'])

# 与训练集的操作类似
X_test_question = tokenizer.texts_to_sequences(test_df['question'])
X_test_question = pad_sequences(X_test_question, maxlen=max_length, padding='post')
X_test_sentence = tokenizer.texts_to_sequences(test_df['sentence'])
X_test_sentence = pad_sequences(X_test_sentence, maxlen=max_length, padding='post')
y_test = test_df['label'].values

# 5. 输入分类模型（LSTM）进行训练
# 创建一个嵌入层（Embedding Layer）对象，用于将文本数据中的单词索引转换为词嵌入表示
embedding_layer = Embedding(vocab_size, embedding_dim, weights=[embedding_matrix], input_length=max_length, trainable=True)

# 定义模型的输入层
input_question = Input(shape=(max_length,))
input_sentence = Input(shape=(max_length,))

# 对输入进行嵌入
question_embedding = embedding_layer(input_question)
sentence_embedding = embedding_layer(input_sentence)

# 构建模型
lstm_layer = LSTM(64, return_sequences=False) # 构建64隐藏层，并且只返回最后一个时间步的输出
question_lstm = lstm_layer(question_embedding)
sentence_lstm = lstm_layer(sentence_embedding)

# 合并两个LSTM的输出
merged = Dense(64, activation='relu')(question_lstm + sentence_lstm)
output = Dense(2, activation='softmax')(merged)

# 定义模型
model = Model(inputs=[input_question, input_sentence], outputs=output)

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# 将标签进行one-hot编码
num_classes = 2
y_train_encoded = np.eye(num_classes)[y_train]
model.fit([X_train_question, X_train_sentence], y_train_encoded, epochs=15, batch_size=32, validation_split=0.25)

# 6. 结果输出
predictions = model.predict([X_test_question, X_test_sentence])
pred_res = np.argmax(predictions, axis=1)
store = []
# 将预测的结果转换为字符数组的形式，方便统计结果
for i in range(len(pred_res)):
    if(pred_res[i] == 0):store.append('entailment')
    else :store.append('not_entailment')
accuracy = np.mean(store == y_test)
print("Accuracy:", accuracy)
