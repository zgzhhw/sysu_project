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

# 使用梯度上升算法获得最优参数
optimal_theta = gradient_ascent(X_train, y_train)

# 在测试集上评估模型
predictions = sigmoid(X_test.dot(optimal_theta))
predictions[predictions >= 0.5] = 1
predictions[predictions < 0.5] = 0

accuracy = np.mean(predictions == y_test)
print(f'Accuracy on test set: {accuracy * 100:.2f}%')
