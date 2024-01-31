import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

class Model:
    def __init__(self, input_size):
        #self.weight = np.random.rand(input_size, 1) #初始化权重矩阵
        self.weight = np.zeros((input_size,1))
        self.bias = 0   #初始化偏置量
        self.loss = []  #初始化损失列表

    def sigmoid(self, x):
        """激活函数"""
        return 1 / (1 + np.exp(-x))

    def forward(self, X):
        """前向传播,计算输出值"""
        temp = np.dot(X, self.weight) + self.bias   #初始输入与权重矩阵进行点积，加上偏置
        output = self.sigmoid(temp) #根据上一步获得的值计算激活函数后的值
        return output   

    def backward(self, x, y, output, learning_rate):
        """反向传播算法"""
        delta = (y - output) * output * (1 - output)    #求偏导的公式
        dw = learning_rate * delta * x.reshape(-1, 1)   #利用矩阵乘法求出dw偏导值
        db = learning_rate * delta  #更新偏置
        loss = (y - output)**2  #获取损失函数值
        return dw, db, loss

    def train(self, X, Y, num_iterations, learning_rate):
        """训练函数"""
        for i in range(num_iterations): #更新迭代每一轮
            sum = 0
            for j in range(len(X)): 
                x = X[j]
                y = Y[j]
                output = self.forward(x)
                dw, db, loss = self.backward(x, y, output, learning_rate)
                self.weight += dw
                self.bias += db
                sum += loss
            self.loss.append(sum)   #将每一轮的损失函数值加入loss列表

    def predict(self, X):
        """根据训练的结果,预测测试集"""
        result = self.forward(X)
        predictions = (result >= 0.5).astype(int)   #如果大于等于0.5则预测为1
        return predictions

    def plot_decision_boundary(self, X, Y, std, mean):
        """将两科成绩和分界线可视化"""
        new_std = np.std(X, axis=0)
        new_mean = np.mean(X, axis=0)
        X = X * std + mean
        admitted = X[Y == 1]
        not_admitted = X[Y == 0]
        plt.scatter(admitted[:, 0], admitted[:, 1], color='green', label='Admitted')
        plt.scatter(not_admitted[:, 0], not_admitted[:, 1], color='red', label='Not Admitted')
        # 绘制分界线
        weight_inverse = self.weight * new_std / np.std(X, axis=0)
        bias_inverse = self.bias - np.dot(np.mean(X, axis=0), weight_inverse)   #逆归一化
        x_min, x_max = X[:, 0].min() - 10, X[:, 0].max() 
        y_min, y_max = X[0, :].min() - 10, X[0, :].max() + 30
        weights = self.weight.reshape(-1)
        boundary_x = np.array([x_min, x_max])
        boundary_y_inverse = -(weight_inverse[0] * boundary_x + bias_inverse) / weight_inverse[1]
        plt.plot(boundary_x, boundary_y_inverse, color='blue', label='Decision Boundary')
        plt.ylim(y_min,y_max)
        plt.xlabel('Exam 1 Score')
        plt.ylabel('Exam 2 Score')
        plt.legend()
        plt.show()

    def plot_show_loss(self,num_iterations):
        """loss函数可视化"""
        plt.plot(range(1, num_iterations + 1), self.loss)
        plt.xlabel('Iterations')
        plt.ylabel('Loss')
        plt.title('Training Loss')
        plt.show()

def read_file(filename):
    """读取并分离输入文件中的信息"""
    data = np.loadtxt(filename, delimiter=',',dtype=float)  
    res = [int(data[i][2]) for i in range(len(data))]
    X = [[data[i][0] , data[i][1]] for i in range(len(data))]
    return np.array(X), np.array(res)

def normalize(X):
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    X_normalized = X / norms
    return X_normalized

# 准备数据
X,Y = read_file('data1.txt')
std = np.std(X, axis=0)
mean = np.mean(X, axis=0)
# 数据归一化
X = (X - np.mean(X, axis=0)) / np.std(X, axis=0)
# 创建逻辑回归模型并进行训练
num_iterations = 1000
input_size = X.shape[1]
model = Model(input_size)
tic = timer()
model.train(X, Y, num_iterations, learning_rate = 0.01)
toc = timer()
# 进行预测
test_data = X
test_data = (test_data - np.mean(X, axis=0)) / np.std(X, axis=0)
predictions = model.predict(test_data)
count = 0
for i in range(len(predictions)):
    pre = predictions[i][0]
    if(pre == Y[i]) : count += 1

print(f"The accuracy is: {count/len(X):.4f}")
print(f'The time spent is: {(toc - tic):.4f} secs')
model.plot_decision_boundary(X, Y, std, mean)
model.plot_show_loss(num_iterations)
