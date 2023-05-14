import pandas as pd
import numpy as np
def check_board(board):
    def check_value(v):
        if v not in ['W','E','B']:
            raise ValueError("参数含有除E,B,W之外的字符")
        return True
    np_check = np.vectorize(check_value)
    return np_check(board)
def boardtodict(board):
    result = []
	
    for i in range(len(board)):
	    for j in range(len(board[i])):
	        if board[i][j] != 'E':
	            result.append({'x': chr(ord('A') + j),'y': str(i + 1),'color': board[i][j]})
class ParameterError(Exception):
    """
    参数错误异常。
    """
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return repr(self.value)
    
class qp:
    def __init__(self):
        pass
    
    @staticmethod
    def board_text_to_list(board:str) -> list:
        """
        将棋盘的文本转为二维数组.

        Args:
            board : 长度为225的文本，只能包含```E B W```三种字符，E表示没有棋子，B表示下了黑棋，W表示下了白棋
            
        Returns:
            返回转换后的15×15的二维列表。
            
        Reises:
            ParameterError:board长度不是225
            ValueError:board包含了非法字符串（```除了E B W之外的```）
        """

        
        if len(board) != 225:
            raise ParameterError("参数长度不是225")
        if not all(x in "EBW" for x in board):
            raise ValueError("参数含有除E,B,W之外的字符")
        df = pd.DataFrame(list(board))
        arr = np.array(df[0]).reshape(15,15).tolist()
        return arr
	
    @staticmethod
    def board_list_to_dict(board:list) -> dict:
        """
        将棋盘的二维数组转为字典.

        Args:
            board : 15*15的数组
            
        Returns:
            返回转换后的字典，注意返回的只有有棋子的x，y，color。
            
        Reises:
            ParameterError:列表长度不是15
            ValueError:board包含了非法字符串（```除了E B W之外的```）
        """

        
        if len(board) != 15:
            raise ParameterError("参数长度不是15")
        res = check_board(board)
        if res == True :
            return boardtodict(board)