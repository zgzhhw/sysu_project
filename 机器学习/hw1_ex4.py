import random
import numpy as np

def monte_carlo_simulation(n, num_simulations):
    success_count = 0  # 记录成功到达点B的次数
    
    for _ in range(num_simulations):
        ant_x, ant_y = 1, 1  # 蚂蚁的初始位置
        visited = set()  # 记录已经访问过的位置
        visited.add((ant_x, ant_y))
        visit_4_4 = 0 # 对位置(4,4)进行特殊判定
        while True:
            # 生成可选择的方向数组
            choices = ['up', 'down', 'left', 'right']
            valid_choices = [] # 合法的移动方向
            
            for c in choices:
                temp_x,temp_y= ant_x,ant_y
                if c == 'up':temp_x -= 1
                elif c == 'down':temp_x += 1
                elif c == 'left':temp_y -= 1
                elif c == 'right' :temp_y += 1

                if temp_x >= 1 and temp_x <= n and temp_y >= 1 and temp_y <= n:
                    if((temp_x, temp_y) == (4, 4) and visit_4_4 <= 1):
                        valid_choices.append(c)
                    elif (temp_x, temp_y) != (4, 4) and (temp_x, temp_y) not in visited:
                        valid_choices.append(c)

            # 没有合法的移动方向时退出
            if len(valid_choices) == 0: break
            direction = random.choice(valid_choices)
            if direction == 'up':
                ant_x -= 1
            elif direction == 'down':
                ant_x += 1
            elif direction == 'left':
                ant_y -= 1
            elif direction == 'right':
                ant_y += 1

            if((ant_x, ant_y) == (4, 4)):visit_4_4 += 1

            # 将当前位置添加到已访问集合中
            visited.add((ant_x, ant_y))
            # 如果蚂蚁成功到达点B，增加成功次数并退出循环
            if (ant_x, ant_y) == (n, n):
                success_count += 1
                break

    # 计算概率P
    probability = success_count / num_simulations
    return probability

# 调用模拟函数
n = 7
num_simulations = 20000

times = 10
res = []
for i in range(times):
    result = monte_carlo_simulation(n, num_simulations)
    res.append(result)
print(res,np.mean(res))