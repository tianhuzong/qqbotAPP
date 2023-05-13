import copy
import json
import numpy as np
from tools import qp
# 定义棋盘大小
BOARD_SIZE = 15

# 定义棋子颜色
BLACK = 'B'
WHITE = 'W'
myqp = qp()
class Board:
    def __init__(self):
        # 初始化棋盘
        self.board = np.full((BOARD_SIZE, BOARD_SIZE), 'E')
        self.player = BLACK
        self.steps = []

    def make_move(self, move):
        # 将落子添加到棋谱中
        self.steps.append(move)
        # 更新棋盘状态
        x, y = move
        self.board[x][y] = self.player
        self.player = BLACK if self.player == WHITE else WHITE

    def unmake_move(self):
        # 悔棋，撤销最后一步落子
        if not self.steps:
            return
        move = self.steps.pop()
        x, y = move
        self.board[x][y] = 'E'
        self.player = BLACK if self.player == WHITE else WHITE

    def is_full(self):
        # 判断棋盘是否已满
        return not np.any(self.board == 'E')

    def is_win(self, x, y):
        # 判断某个位置是否形成连续的五子棋
        color = self.board[x][y]
        slice_directions = [self.board[x: x+5, y], # 竖直方向
                           self.board[x, y: y+5], # 水平方向
                           np.diagonal(self.board, y-x)[max(0, y-x):min(BOARD_SIZE-x, BOARD_SIZE-y)+4], # 对角线方向
                           np.diagonal(np.rot90(self.board), BOARD_SIZE-1-y+x)[max(0, BOARD_SIZE-1-y+x-4):min(x, BOARD_SIZE-y)-1:-1]] # 反对角线方向
        for direction in slice_directions:
            if direction.size < 5:
                continue
            counts = np.where(direction == color, 1, 0)
            if np.sum(counts) >= 5:
                return True
        return False

    def get_score(self, player):
        # 根据当前棋盘状态计算玩家的得分
        return np.sum(self.board == player)

    def get_all_moves(self, player):
        # 获取当前玩家可以下的所有合法落子位置
        mask = self.board == 'E'
        if player == BLACK:
            mask &= np.apply_along_axis(lambda arr: any([i == BLACK for i in arr]), 1, self.board)[:, np.newaxis]
        else:
            mask &= (self.board == -1)
        return list(zip(*np.where(mask)))

    def has_neighbour(self, x, y, color):
        # 判断指定位置周围是否有同色棋子
        if x > 0 and self.board[x-1][y] == color:
            return True
        if x < BOARD_SIZE-1 and self.board[x+1][y] == color:
            return True
        if y > 0 and self.board[x][y-1] == color:
            return True
        if y < BOARD_SIZE-1 and self.board[x][y+1] == color:
            return True
        if x > 0 and y > 0 and self.board[x-1][y-1] == color:
            return True
        if x < BOARD_SIZE-1 and y < BOARD_SIZE-1 and self.board[x+1][y+1] == color:
            return True
        if x > 0 and y < BOARD_SIZE-1 and self.board[x-1][y+1] == color:
            return True
        if x < BOARD_SIZE-1 and y > 0 and self.board[x+1][y-1] == color:
            return True
        return False

def alphabeta(board, depth, alpha, beta, player, max_player):
    # 判断是否达到搜索深度
    if depth == 0:
        # 返回当前局面得分（此处可以根据需要进行修改，比如使用神经网络模型进行估值）
        score = board.get_score(max_player)
        return score, None

    # 如果是极大层，我们要找到最大价值的棋步
    if player == max_player:
        best_score = -float('inf')
        best_move = None
        for move in board.get_all_moves(max_player):
            # 尝试在 (x,y) 上下子
            board.make_move(move)
            # 递归计算子节点的分数
            score, _ = alphabeta(board, depth-1, alpha, beta, BLACK if player == WHITE else WHITE, max_player)
            # 恢复棋盘状态
            board.unmake_move()
            # 更新最大价值
            if score > best_score:
                best_score = score
                best_move = move
            # 执行剪枝操作
            if best_score >= beta:
                return best_score, best_move
            alpha = max(alpha, best_score)
        return best_score, best_move

    # 如果是极小层，我们要找到最小价值的棋步
    else:
        best_score = float('inf')
        best_move = None
        for move in board.get_all_moves(max_player):
            # 尝试在 (x,y) 上下子（对手执另一种棋子）
            board.make_move(move)
            # 递归计算子节点的分数
            score, _ = alphabeta(board, depth-1, alpha, beta, BLACK if player == WHITE else WHITE, max_player)
            # 恢复棋盘状态
            board.unmake_move()
            # 更新最小价值
            if score < best_score:
                best_score = score
                best_move = move
            # 执行剪枝操作
            if best_score <= alpha:
                return best_score, best_move
            beta = min(beta, best_score)
        return best_score, best_move

def predict(board_str, color):
    # 解析棋盘状态
    board = Board()
    #rows = board_str.strip().split('\n')
    rows = myqp.board_text_to_list(board_str)
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if rows[i][j] == 'B':
                board.board[i][j] = BLACK
            elif rows[i][j] == 'W':
                board.board[i][j] = WHITE

    # 设置当前玩家执棋子颜色
    player = BLACK if color == 'B' else WHITE

    # 调用极大极小值算法获取下一步落子位置
    _, best_move = alphabeta(board, depth=3, alpha=-float('inf'), beta=float('inf'), player=player, max_player=player)

    if player == BLACK:
        # 将下一步落子位置转换为字符串格式
        x, y = best_move
        x_letter = chr(x + 65)
        y_number = str(y + 1)
    else:
        # 在预测之前判断哪些地方不能下，将不能下的位置设置为 -1，避免在计算得分时误判
        board.board[board.board != 'E'] = -1
        board.board[board.board == 'E'] = 0

        mask = np.apply_along_axis(lambda arr: any([i == WHITE for i in arr]), 1, board.board)[:, np.newaxis]
        mask &= (board.board != -1)
        best_move = np.unravel_index(np.argmax(np.where(mask, board.board, 0)), board.board.shape)

        # 将下一步落子位置转换为字符串格式
        x, y = best_move
        x_letter = chr(x + 65)
        y_number = str(y + 1)

    # 构建返回结果，即下一步应该下在哪个位置，并将其转换为字符串格式
    result = {'x': x_letter, 'y': y_number}
    return result