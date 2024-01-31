import re
import copy
from collections import Counter
from numpy import Infinity as inf

White = (255,255,255)
Black = (0,0,0)

class Evaluation:
    def __init__(self,board):
        self.size = 15
        self.chess_type = 7
        self.pos = [[(7 - max(abs(x - 7), abs(y - 7))) for x in range(15)] for y in range(15)]
        self.record = [[[0,0,0,0] for x in range(self.size)] for y in range(self.size)]
        self.count = [[0 for x in range(self.chess_type)] for y in range(2)]
        self.board = board
        self.pattern_white = {
        "22222" : "five", #连五 white
        "022220": "live_four", #活四 white
        "122220|202221|122022":"skip_four", #冲四 white
        "02220|020220":"live_three" ,#活三 white
        "122200|122020|120220|22002|20202|1022201" : "sleep_three", #眠三 white
        "002200|02020|020020" : "live_two", #活二 white
        "122000|120200|120020|20002|1200021|1020021|1002021|1002201|1020201" : "sleep_two", #眠二 white
        }
        self.pattern_black = {
        "11111" : "five", #连五 black
        "011110": "live_four", #活四 black
        "211110|101112|211011":"skip_four", #冲四 black
        "01110|010110":"live_three"  ,#活三 black
        "211100|211010|210110|11001|10101|2011102" : "sleep_three", #眠三 black
        "001100|01010|010010" : "live_two", #活二 black
        "211000|210100|210010|10001|2100012|2010012|2001012|2001102|2010102" : "sleep_two", #眠二 black
        }
    
    def reset(self):
        '''重置函数'''
        for y in range(self.size):
            for x in range(self.size):
                for i in range(4):
                    self.record[y][x][i] = 0
        for i in range(len(self.count)):
            for j in range(len(self.count[0])):
                self.count[i][j] = 0



    def evaluate(self,board,patterns):
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
        scores = Counter()
        for line in all_lines:
            for pattern, score in patterns.items():
                if re.search(pattern, line):
                    scores[score] += 1
        return scores
    
    def calculate(self,board,scores_w,scores_b):
        if(scores_b["five"] != 0):return 100000
        if(scores_w["five"] != 0):return -100000
        if(scores_b["live_four"] != 0):return 10000
        if(scores_b["skip_four"] != 0):return 9980
        if(scores_b["live_three"] != 0 and scores_w["skip_four"]):return 9950
        if(scores_w["live_four"] != 0):return -9970
        if(scores_w["live_three"] != 0 and scores_w["skip_four"]):return -9960
        if(scores_w["live_three"]>1 and scores_b["skip_four"] == 0 and scores_b["live_three"] ==0 and scores_b["sleep_three"]):return -9940
        score1 = 0
        for key in scores_w:
            if(key == "live_three" and scores_w[key] > 1):score1 += 2000
            if(key == "live_three" and scores_w[key] == 1):score1 += 200
            if(key == "skip_four"):score1 += scores_w[key]*10
            if(key == "live_two"):score1 += scores_w[key]*4
            if(key == "skip_two"):score1 += scores_w[key]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j] == 2):score1 += self.pos[i][j]

        score2 = 0
        for key in scores_b:
            if(key == "live_three" and scores_w[key] > 1):score2 += 500
            if(key == "live_three" and scores_w[key] == 1):score1 += 100
            if(key == "skip_four"):score1 += scores_w[key]*10
            if(key == "live_two"):score1 += scores_w[key]*4
            if(key == "skip_two"):score1 += scores_w[key]
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j] == 1):score2 += self.pos[i][j]

        return -score1 + score2

def create_move(pos,board):
        '''生成移动序列'''
        moves = []
        for i in range(len(board)):
            for j in range(len(board[i])):
                if(board[i][j]==0):moves.append((pos[i][j],i,j))
        moves.sort(reverse = True)
        return moves

def AlphaBetaSearch(board, alpha, beta, turn, depth):
    test = Evaluation(board)
    moves = create_move(test.pos,board)
    best_score = inf if turn == 0 else -inf
    best_move = None
    if(depth == 0 or len(moves) == 0):
        return best_move,test.calculate(board,test.evaluate(board, test.pattern_white), test.evaluate(board,test.pattern_black))
    if(turn == 1):
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m[1]][m[2]] = 1
            value = AlphaBetaSearch(new_board, alpha, beta, 0, depth-1)[1]
            if(value > best_score):
                best_score , best_move = value ,m
            alpha = max(alpha,best_score)
            if(alpha >= beta):break

    else:
        for m in moves:
            new_board = copy.deepcopy(board)
            new_board[m[1]][m[2]] = 2
            value = AlphaBetaSearch(new_board, alpha, beta, 1, depth-1)[1]
            if(value < best_score):
                best_score , best_move = value , m
            beta = min(beta,best_score)
            if(alpha >= beta):break
    
    return best_move,best_score 
