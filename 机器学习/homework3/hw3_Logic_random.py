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

# 随机梯度上升算法
def stochastic_gradient_ascent(X, y, learning_rate=0.00005, epochs=10000):
    theta = np.zeros(X.shape[1])
    length = len(y)
    losses = []  # 用于存储每次迭代的损失值
    for epoch in range(epochs):
        total_loss = 0
        for i in range(length):
            rand_index = np.random.randint(0, length)  # 随机选择一个样本
            h = sigmoid(X[rand_index].dot(theta))      # 计算预测值的sigmoid
            gradient = X[rand_index].T * (h - y[rand_index])  # 计算梯度
            theta -= learning_rate * gradient           # 更新theta
            total_loss += compute_loss(X, y, theta)     # 计算总损失
        avg_loss = total_loss / length
        losses.append(avg_loss)
        if epoch % 1000 == 0:
            print(f'Epoch: {epoch}, Loss: {avg_loss}')
    return theta, losses

# 使用随机梯度上升算法获得最优参数和损失值列表
optimal_theta, losses = stochastic_gradient_ascent(X_train, y_train)

# 绘制损失值随迭代次数的变化图表
plt.figure(figsize=(8, 6))
plt.plot(range(len(losses)), losses, color='b')
plt.xlabel('Iteration Number')
plt.ylabel('Objective Value')
plt.title('Objective Function on Each Iteration of Stochastic Gradient Ascent')
plt.show()

# 在测试集上评估模型
predictions = sigmoid(X_test.dot(optimal_theta))
predictions[predictions >= 0.5] = 1
predictions[predictions < 0.5] = 0

accuracy = np.mean(predictions == y_test)
print(f'Accuracy on test set: {accuracy * 100:.2f}%')
