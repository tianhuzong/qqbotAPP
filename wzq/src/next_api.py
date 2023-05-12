import json

# ����������
BOARD_SIZE = 15 

# ����Сֵ�㷨
def minimax(board, depth, player, max_player):
    # �ж��Ƿ�ﵽ�������
    if depth == 0:
        # ���ص�ǰ����÷֣��˴����Ը�����Ҫ�����޸ģ�����ʹ��������ģ�ͽ��й�ֵ��
        return 0

    # ��ȡ��ǰ��ң�����/���ӣ���ִ������ɫ
    color = 'B' if player == 1 else 'W'

    # ����Ǽ���㣬����Ҫ�ҵ�����ֵ���岽
    if player == max_player:
        best_score = -float('inf')
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 'E':
                    # ������ (x,y) ������
                    board[x][y] = color
                    # �ݹ�����ӽڵ�ķ���
                    score = minimax(board, depth-1, 3-player, max_player)
                    # �ָ�����״̬
                    board[x][y] = 'E'
                    # ��������ֵ����¼��ʱӦ�����ӵ�λ��
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)
        return best_score
    
    # ����Ǽ�С�㣬����Ҫ�ҵ���С��ֵ���岽
    else:
        worst_score = float('inf')
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if board[x][y] == 'E':
                    # ������ (x,y) �����ӣ�����ִ��һ����ɫ�����ӣ�
                    board[x][y] = 'B' if color=='W' else 'W'
                    # �ݹ�����ӽڵ�ķ���
                    score = minimax(board, depth-1, 3-player, max_player)
                    # �ָ�����״̬
                    board[x][y] = 'E'
                    # ������С��ֵ����¼��ʱӦ�����ӵ�λ��
                    if score < worst_score:
                        worst_score = score
                        best_move = (x, y)
        return worst_score

# ���ݶԾ����ݼ�����һ������λ��
def next_move(json_string, color, depth=3):
    # ������ĸ�����ֵ�ӳ���
    x_map = {chr(i+65): i for i in range(BOARD_SIZE)}
    y_map = {str(i+1): i for i in range(BOARD_SIZE)}
    # ����json����
    data = json.loads(json_string)
    # ������ά��������
    board = [[data['board'][i+j*BOARD_SIZE] for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    # ���õ�ǰ���ִ������ɫ
    player = 1 if color == 'B' else 2
    # ���ü���Сֵ�㷨��ȡ��һ������λ��
    best_move = minimax(board, depth, player, player)
    # ����һ������λ��ת��Ϊ��ĸ�����������ʽ
    x, y = best_move[0], best_move[1]
    x_letter = chr(x + 65)
    y_number = str(y + 1)
    # �������ؽ��������һ��Ӧ�������ĸ�λ�ã�������ת��Ϊ�ַ�����ʽ
    result = {'x': x_letter, 'y': y_number}
    return json.dumps(result)