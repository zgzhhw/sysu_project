import random
import numpy as np
import math

times = 100 # 训练次数
nums = [20, 50, 100, 200, 300, 500, 1000, 5000] #投点个数数组
count = 0

for num in nums:
    nums_of_pi = []
    for t in range(times):
        count = 0
        for i in range(num):
            x = random.random()
            y = random.random()
            if(x**2 + y**2 <= 1):
                count += 1
        PI = count * 4 / num
        nums_of_pi.append(PI)
    print(f"With the node number: {num} \n\
        The mean value is : {np.mean(nums_of_pi):.4f},\n\
        The var is : {np.var(nums_of_pi) :.4f}\n\
        The loss is {100 * abs(math.pi - np.mean(nums_of_pi)) / math.pi :.4f}%")




