import pandas as pd
import numpy as np

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
        将棋盘的二进制数据转为二维数组.

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