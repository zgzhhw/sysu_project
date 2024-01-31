import re
import copy
from collections import Counter

# 定义正则表达式模式和对应的棋型分值
patterns = {
    "11111" : "连五 black", #连五 black
    "22222" : "连五 white", #连五 white
    "011110": "活四 black", #活四 black
    "022220": "活四 white", #活四 white
    "211110|10111|11011":"冲四 black", #冲四 black
    "122220|20222|22022":"冲四 white", #冲四 white
    "01110|1011":"活三 black" ,#活三 black
    "02220|2022":"活三 white" ,#活三 white
    "211100|211010|210110|11001|10101|2011102" : "#眠三 black", #眠三 black
    "122200|122020|120220|22002|20202|1022201" : "眠三 white", #眠三 white
    "001100|01010|1001" : "活二 black", #活二 black
    "002200|02020|2002" : "活二 white", #活二 white
    "211000|210100|210010|10001" : "眠二 black", #眠二 black
    "122000|120200|120020|20002" : "眠二 white", #眠二 white
}

# 遍历棋盘
board = [
    [1, 2, 1, 2, 1, 2, 1, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 2, 1, 2, 1, 2, 0, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 2, 1, 0, 2, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 2, 1, 2, 1, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
]


rows = len(board)
cols = len(board[0])
all_lines = []

for i in range(rows):
    line = "".join(str(x) for x in board[i])
    line_r = line[::-1]
    all_lines.append(line)
    if(line != line_r):all_lines.append(line_r)
    
for j in range(cols):
    line = "".join(str(board[i][j]) for i in range(rows))
    line_r = line[::-1]
    all_lines.append(line)
    if(line != line_r):all_lines.append(line_r)
    
for k in range(-rows+1, cols):
    line = "".join(str(board[i][i+k]) for i in range(rows) if 0 <= i+k < cols)
    line_r = line[::-1]
    all_lines.append(line)
    if(line != line_r):all_lines.append(line_r)
    
for k in range(rows+cols-1):
    line = "".join(str(board[i][k-i]) for i in range(rows) if 0 <= k-i < cols)
    line_r = line[::-1]
    all_lines.append(line)
    if(line != line_r):all_lines.append(line_r)

# 匹配棋型并计算分值
scores = Counter()
for line in all_lines:
    for pattern, score in patterns.items():
        if re.search(pattern, line):
            scores[score] += 1


# 打印结果
print(scores)
