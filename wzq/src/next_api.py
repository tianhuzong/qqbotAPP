import json

# 五子棋棋盘
BOARD_SIZE = 15 

# 极大极小值算法
def minimax(board, depth, player, max_player):
    # 判断是否达到搜索深度
    if depth == 0:
        # 返回当前局面得分（此处可以根据需要进行修改，比如使用神经网络模型进行估值）
        return 0

    # 获取当前玩家（黑子/白子）所执棋子颜色
    color = 'B' if player == 1 else 'W'

    # 如果是极大层，我们要找到最大价值的棋步
    if player == max_player:
        best_score = -float('inf')
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 'E':
                    # 尝试在 (x,y) 上下子
                    board[x][y] = color
                    # 递归计算子节点的分数
                    score = minimax(board, depth-1, 3-player, max_player)
                    # 恢复棋盘状态
                    board[x][y] = 'E'
                    # 更新最大价值并记录此时应该下子的位置
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        return best_score
    
    # 如果是极小层，我们要找到最小价值的棋步
    else:
        worst_score = float('inf')
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 'E':
                    # 尝试在 (x,y) 上下子（对手执另一种颜色的棋子）
                    board[x][y] = 'B' if color=='W' else 'W'
                    # 递归计算子节点的分数
                    score = minimax(board, depth-1, 3-player, max_player)
                    # 恢复棋盘状态
                    board[x][y] = 'E'
                    # 更新最小价值并记录此时应该下子的位置
                    if score < worst_score:
                        worst_score = score
                        best_move = (x, y)
        return worst_score

# 根据对局数据计算下一步落子位置
def next_move(json_string, color, depth=3):
    # 定义字母到数字的映射表
    x_map = {chr(i+65): i for i in range(BOARD_SIZE)}
    y_map = {str(i+1): i for i in range(BOARD_SIZE)}
    # 解析json数据
    data = json.loads(json_string)
    # 构建二维棋盘数组
    board = [[data['board'][i+j*BOARD_SIZE] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    # 设置当前玩家执棋子颜色
    player = 1 if color == 'B' else 2
    # 调用极大极小值算法获取下一步落子位置
    best_move = minimax(board, depth, player, player)
    # 将下一步落子位置转换为字母数字坐标的形式
    x, y = best_move[0], best_move[1]
    x_letter = chr(x + 65)
    y_number = str(y + 1)
    # 构建返回结果，即下一步应该下在哪个位置，并将其转换为字符串格式
    result = {'x': x_letter, 'y': y_number}
    return json.dumps(result)