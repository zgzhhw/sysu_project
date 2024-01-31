import matplotlib.pyplot as plt

# 给定的召回率和精确率数据
Recall = [1/7, 2/7, 2/7, 3/7, 4/7, 5/7, 5/7, 6/7, 6/7, 1]
Precision = [1, 1, 2/3, 3/4, 4/5, 5/6, 5/7, 6/8, 6/9, 7/10]

# 绘制P-R曲线
plt.figure(figsize=(8, 6))
plt.plot(Recall, Precision, marker='o', color='b', linestyle='-', linewidth=2)
plt.xlabel('Recall')
plt.ylabel('Precision')
plt.title('P-R Curve')
plt.grid(True)
plt.show()
