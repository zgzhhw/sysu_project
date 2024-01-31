import random

'''模拟函数'''
def simulate():
    if random.random() < 0.5: # 一半的概率进入组件A
        if random.random() < 0.85:# 表示A组件成功
            return True
        else :
            return False    
    else :  # 另一半时间进入组件B
        if random.random() < 0.95 and random.random() < 0.9: # 表示BC组件成功
            return True
        else :
            return False

'''改进后的模拟函数'''
def simulate_change():
    if random.random() < 0.85:# 表示A组件成功
        return True   
    if random.random() < 0.95 and random.random() < 0.9: # 表示BC组件成功
        return True
    else :
        return False

simu_times = 10000
succ_times = 0
for i in range(simu_times):
    if simulate_change() == True:
        succ_times += 1

print(f"The reliability of the system simulated is:{succ_times / simu_times:.4f}")