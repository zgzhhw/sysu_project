import random
import numpy as np
import math
from scipy.integrate import dblquad

times = 100 # 训练次数
samples = [10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 500] #采样次数
count = 0

x_low_bound = 2
y_low_bound = -1
x_up_bound = 4
y_up_bound = 1
z_max = 3**15   # 利用求偏导对上界进行粗略估计，为了方便采用整数作为底

def func(y, x):
    return (y**2 * math.e**(-y**2) + x**4 * math.e**(-x**2)) / (x * math.e**(-x**2))

# 通过调用py内置的求二重积分的函数进行求解
result, _ = dblquad(func, x_low_bound, x_up_bound, lambda x: y_low_bound, lambda x: y_up_bound)
print(f"The standard result is:{result}")

base_area = (y_up_bound - y_low_bound) * (x_up_bound - x_low_bound) * z_max
for sample in samples:
    res = []
    for t in range(times):
        count = 0
        for i in range(sample):
            x = random.uniform(x_low_bound, x_up_bound)
            y = random.uniform(y_low_bound, y_up_bound)
            z = random.uniform(0, z_max)
            if( z <= func(y, x)):
                count += 1
        value = count / sample # 求出落点分布在函数中的概率
        res.append(value * base_area) # 将概率×基本体积，得到积分的值
    print(f"With the node number: {sample:.4f} \n\
        The mean value is : {np.mean(res):.4f}\n\
        The var is : {np.var(res):.4f}\n\
        The loss is : {abs(result - np.mean(res)) / result :.4f}")