import re
from collections import Counter
from numpy import Infinity as inf

node_num = 0 #全局变量，统计搜索的节点数量
White = (255,255,255)
Black = (0,0,0)
pos = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(15)] for y in range(15)]
#将棋盘的每个位置赋予权值，中心为7，往外扩展一圈则递减1
pattern_white = {
    "22222" : "five", #连五 white
    "022220": "live_four", #活四 white
    "122220|120222|122022|122202|022221|222021|220221|202221":"skip_four", #冲四 white
    "022020|02220|020220":"live_three" ,#活三 white
    "002221|020221|022021|20022|20202|1022201" : "sleep_three", #眠三 white
    "002200|020200|020020|002020" : "live_two", #活二 white
    "122000|120200|120020|20002|1200021|1020021|1002021|1002201|1020201" : "sleep_two", #眠二 white
    } #模式匹配串，方便进行正则匹配
pattern_black = {
    "11111" : "five", #连五 black
    "011110": "live_four", #活四 black
    "211110|210111|211011|211101|011112|111012|110112|101112":"skip_four", #冲四 black
    "011010|01110|010110":"live_three"  ,#活三 black
    "001112|010112|011012|10011|10101|2011102" : "sleep_three", #眠三 black
    "001100|010100|010010|001010" : "live_two", #活二 black
    "211000|210100|210010|10001|2100012|2010012|2001012|2001102|2010102" : "sleep_two", #眠二 black
    }

def evaluate(board,patterns):
    """返回pattern相应的匹配字典"""
    rows = len(board)
    cols = len(board[0])
    all_lines = []
    for i in range(rows):   #将每一行转换为字符串
        line = "".join(str(x) for x in board[i])
        all_lines.append(line)
    for j in range(cols):   #将每一列转换为字符串
        line = "".join(str(board[i][j]) for i in range(rows))
        all_lines.append(line)
    for k in range(-rows+1, cols):  #将每一左斜行转换为字符串
        line = "".join(str(board[i][i+k]) for i in range(rows) if 0 <= i+k < cols)
        all_lines.append(line)
    for k in range(rows+cols-1):    #将每一右斜行转换为字符串
        line = "".join(str(board[i][k-i]) for i in range(rows) if 0 <= k-i < cols)
        all_lines.append(line)
    scores = Counter()  #调用counter函数，统计每种棋形的个数，以字典的方式存储
    for line in all_lines:
        for pattern, score in patterns.items():
            if re.search(pattern, line):    #进行正则匹配
                scores[score] += 1
    return scores   #返回存储了各种棋形以及其个数的字典
    
def calculate(pos,board,scores_mine,scores_opponent):
    """分数计算函数"""
    score1 = 0  #自己方的分数的初始化
    for key in scores_mine: 
        #遍历存储了自己棋形的字典并赋分
        if(key == "five"):return 10000000   #遇到连五直接返回
        if(key == "skip_four" and scores_mine[key] > 1):score1 += 1000000
        if(key == "live_four"):score1 += 40000
        if(key == "skip_four"):score1 += 10000
        if(key == "live_three" and scores_mine[key] > 1):score1 += 3000
        if(key == "live_three" and scores_mine[key] == 1):score1 += 500
        if(key == "live_two" and scores_mine[key] > 1):score1 += 40
        if(key == "live_two" and scores_mine[key] == 1):score1 += 40
        if(key == "sleep_two"):score1 += scores_mine[key]
    if("live_three" in scores_mine and "sleep_three" in scores_mine):score1 += 1000*scores_mine["sleep_three"]
    if("live_three" in scores_mine and "live_two" in scores_mine):score1 += 500*scores_mine["live_two"]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == 1): score1 += pos[i][j]
    score2 = 0
    for key in scores_opponent:
        if(key == "five"):return  -10000000
        if(key == "skip_four" and scores_opponent[key] > 1):score2 += 100000
        if(key == "live_four"):score2 += 40000
        if(key == "skip_four"):score2 += 10000
        if(key == "live_three" and scores_opponent[key] > 1):score2 += 3000
        if(key == "live_three" and scores_opponent[key] == 1):score2 += 500
        if(key == "live_two" and scores_opponent[key] > 1):score2 += 40
        if(key == "live_two" and scores_opponent[key] == 1):score2 += 40
        if(key == "sleep_two"):score2 += scores_opponent[key]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if(board[i][j] == 2): score2 += pos[i][j]
    return  4*score1 - score2   #调整参数，使其更富于进攻性

def evaluate_point(board,x,y,turn,patterns):
    """统计当前落点的四个方向的棋形及个数,方便连五的特判和返回"""
    lines = []
    line = "".join(str(board[x][i]) for i in range(15))
    lines.append(line)
    line = "".join(str(board[i][y]) for i in range(15))
    lines.append(line)
    line = "".join(str(board[x+k][y+k]) for k in range(-15,15) if 0<=x+k<15 and 0<=y+k<15)
    lines.append(line)
    line = "".join(str(board[x+k][y-k]) for k in range(-15,15) if 0<=x+k<15 and 0<=y-k<15)
    lines.append(line)
    scores = Counter()
    for line in lines:
        for pattern, score in patterns.items():
            if re.search(pattern, line):
                scores[score] += 1
    return scores

def create_move(pos,board,turn):
        '''生成移动序列'''
        moves = []
        left = 15
        right = 0
        up = 15
        down = 0    #初始化边界值
        flag = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j] != 0):
                    left = min(left,j)
                    right = max(right,j)
                    up = min(i,up)
                    down = max(i,down)
                    flag = 1
        #统计当前落子集群的上下左右边界
        if(flag == 0):  #如果棋盘上没有落子，则直接下在中间的位置(先手)
            moves.append((7,7,7))
            return moves
        if(left - 1 >= 0):left -= 1
        if(right + 1 < len(board)):right += 1
        if(up - 1 >= 0): up -= 1
        if(down + 1 < len(board)):down += 1
        #对上面统计的边界进行扩展，提高其落子的准确性
        for i in range(up,down+1):
            for j in range(left,right+1):
                if(board[i][j]==0): moves.append((pos[i][j],i,j))   #将落点的位置权重作为排序依据加入到列表中
        moves.sort(reverse = True)  #对列表进行排序，优先选择靠近中间的落点
        return moves

def AlphaBetaSearch(board, alpha, beta, turn, depth):
    """剪枝函数"""
    global node_num 
    node_num += 1   #利用全局变量统计搜索的节点
    moves = create_move(pos,board,turn) #生成可移动序列
    best_score = inf if turn == 0 else -inf #定义best_score
    best_move = None    #定义best_move
    if(depth == 0 or len(moves) == 0):  #终止条件判断
        oppo = evaluate(board,pattern_white)  #对手的棋形
        mine = evaluate(board,pattern_black)  #自己的棋形
        value = calculate(pos,board,mine,oppo)
        return  best_move, value,node_num  #计算分数返回
    #轮数的判定和剪枝
    if(turn == 1):
        for m in moves:
            board[m[1]][m[2]] = 1   #模拟在此位置进行落点
            cur = evaluate_point(board, m[1], m[2], turn, pattern_black)    #计算此位置是否形成连五
            if("five" in cur):  #如果已经有，则撤销上一步操作，直接返回
                board[m[1]][m[2]] = 0
                return m,10000000,node_num
            value = AlphaBetaSearch(board, alpha, beta, 0, depth-1)[1]  #递归调用函数，计算value值
            board[m[1]][m[2]] = 0   #回溯，撤销上一步的操作
            if(value > best_score): #对于自己方，如果value大于当前的best_score，则更新best_move 和 best_score
                best_score , best_move = value ,m
            alpha = max(alpha,best_score)   #更新alpha值
            if(alpha >= beta):break    #进行判断剪枝
    else:
        #白棋进行落子，操作与上面的对称
        for m in moves:
            board[m[1]][m[2]] = 2
            cur = evaluate_point(board, m[1], m[2], turn, pattern_white)
            if("five" in cur):
                board[m[1]][m[2]] = 0
                return m,-10000000,node_num
            value = AlphaBetaSearch(board, alpha, beta, 1, depth-1)[1]
            board[m[1]][m[2]] = 0
            if(value < best_score):
                best_score , best_move = value , m
            beta = min(beta,best_score)
            if(alpha >= beta):break

    return best_move,best_score,node_num    #返回
