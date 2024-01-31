import numpy as np
import matplotlib.pyplot as plt

# 读取训练数据
train_data = np.loadtxt('homework3\dataForTrainingLogistic.txt')
X_train = train_data[:, :-1]  # 特征
y_train = train_data[:, -1]    # 标签

# 添加偏置项到特征矩阵
X_train = np.c_[np.ones(X_train.shape[0]), X_train]

# 读取测试数据
test_data = np.loadtxt('homework3\dataForTestingLogistic.txt')
X_test = test_data[:, :-1]
y_test = test_data[:, -1]
X_test = np.c_[np.ones(X_test.shape[0]), X_test]

# 定义sigmoid函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 定义损失函数（条件对数似然）
def compute_loss(X, y, theta):
    length = len(y)
    h = sigmoid(X.dot(theta))
    loss = -1/length * (y.dot(np.log(h)) + (1 - y).dot(np.log(1 - h)))
    return loss

def gradient_ascent(X, y, learning_rate=0.001, epochs=10000):
    theta = np.zeros(X.shape[1])
    length = len(y)
    for epoch in range(epochs):
        h = sigmoid(X.dot(theta))               # 计算预测值的sigmoid
        gradient = 1/length * X.T.dot(h - y)    # 矩阵求导
        theta -= learning_rate * gradient       # 更新theta
        # 计算损失
        loss = compute_loss(X, y, theta)
        if epoch % 1000 == 0:
            print(f'Epoch: {epoch}, Loss: {loss}')
    return theta

k_values = range(10, 401, 10)
train_errors = []
test_errors = []

for k in k_values:
    # 随机选择大小为k的训练子集
    random_indices = np.random.choice(len(X_train), k, replace=False)
    X_train_subset = X_train[random_indices]
    y_train_subset = y_train[random_indices]
    
    # 使用梯度上升算法获得最优参数
    optimal_theta = gradient_ascent(X_train_subset, y_train_subset)
    
    # 在当前训练子集上计算训练误差
    train_predictions = sigmoid(X_train_subset.dot(optimal_theta))
    train_predictions[train_predictions >= 0.5] = 1
    train_predictions[train_predictions < 0.5] = 0
    train_error = np.mean(train_predictions != y_train_subset)
    train_errors.append(train_error)
    
    # 在测试集上计算测试误差
    test_predictions = sigmoid(X_test.dot(optimal_theta))
    test_predictions[test_predictions >= 0.5] = 1
    test_predictions[test_predictions < 0.5] = 0
    test_error = np.mean(test_predictions != y_test)
    test_errors.append(test_error)

# 绘制图表
plt.figure(figsize=(10, 6))
plt.plot(k_values, train_errors, label='Training Error', color='blue')
plt.plot(k_values, test_errors, label='Test Error', color='red')
plt.xlabel('Training Set Size (k)')
plt.ylabel('Error')
plt.legend()
plt.title('Training and Test Error vs. Training Set Size')
plt.show()
