import random
import numpy as np
times = 100 # 训练次数
samples = [5, 10, 20, 30, 40, 50, 60, 70, 80, 100] #采样次数
count = 0

for sample in samples:
    res = []
    for t in range(times):
        count = 0
        for i in range(sample):
            x = random.random()
            y = random.random()
            if(y <= x**3):
                count += 1
        value = count / sample
        res.append(value)
    print(f"With the node number: {sample} \n\
        The mean value is : {np.mean(res):.4f},\n\
        The var is : {np.var(res) :.4f}\n\
        The loss is {100 * abs(1 / 4 - np.mean(res)) / 0.25 :.4f}%")





