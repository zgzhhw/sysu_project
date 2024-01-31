import numpy as np
import matplotlib.pyplot as plt

# 读取训练数据
train_data = np.loadtxt('homework3\dataForTrainingLinear.txt')
X_train = train_data[:, :-1]  # 特征
y_train = train_data[:, -1]    # 目标

# 添加偏置项到特征矩阵
X_train = np.c_[np.ones(X_train.shape[0]), X_train]

# 读取测试数据
test_data = np.loadtxt('homework3\dataForTestingLinear.txt')
X_test = test_data[:, :-1]
y_test = test_data[:, -1]
X_test = np.c_[np.ones(X_test.shape[0]), X_test]

# 定义随机梯度下降函数
def stochastic_gradient_descent(X, y, learning_rate=0.00015, epochs=1500000, batch_size=1):
    theta = np.zeros(X.shape[1])  # 初始化参数
    training_errors = []  # 用于保存每迭代100000步的训练误差
    test_errors = []  # 用于保存每迭代100000步的测试误差
    predictions = []  # 用于保存每迭代100000步的预测值
    for epoch in range(1, epochs + 1):
        # 随机选择batch_size个样本
        indices = np.random.choice(X.shape[0], batch_size, replace=False)
        X_batch = X[indices]
        y_batch = y[indices]
        error = y_batch - np.dot(X_batch, theta)
        theta += learning_rate * (X_batch.T.dot(error) / batch_size)
        # 计算每迭代100000步的训练误差、测试误差和预测值
        if epoch % 100000 == 0:
            training_errors.append(np.mean(error ** 2))
            test_error = y_test - np.dot(X_test, theta)
            test_errors.append(np.mean(test_error ** 2))
            predictions.append(np.dot(X_test, theta))
            print(f"--------epoch:{epoch / 100000}--------")
            print(f"training_error:{training_errors[-1]}")
            print(f"testing_error:{test_errors[-1]}")
            print(f"Parameters (theta):[{theta}]")
    return theta, training_errors, test_errors, predictions

# 训练模型并获取参数、训练误差列表、测试误差列表和预测值列表
theta, training_errors, test_errors, predictions = stochastic_gradient_descent(X_train, y_train)

# 绘制训练误差和测试误差随迭代次数的变化图
plt.figure(figsize=(10, 6))
plt.plot(range(100000, 1500001, 100000), training_errors, color='blue', label='Training Error')
plt.plot(range(100000, 1500001, 100000), test_errors, color='red', label='Test Error')
plt.xlabel('Iterations')
plt.ylabel('Mean Squared Error')
plt.title('Training and Test Error over Iterations (SGD)')
plt.legend()
plt.grid(True)
plt.show()

# 绘制预测值和实际值的可视化
plt.figure(figsize=(10, 6))
for i in range(len(predictions)):
    plt.plot(y_test, predictions[i], marker='o', linestyle='-', label=f'Iteration {i+1}')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual Prices vs. Predicted Prices (SGD)')
plt.legend()
plt.grid(True)
plt.show()

print("The final Parameters (theta) using SGD:", theta)
