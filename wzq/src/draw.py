from PIL import Image
import numpy as np
import cv2

def draw_piece(board_array, x, y, color):
    """在棋盘图像上绘制棋子。

    Args:
        board_array: 棋盘图像的Numpy数组表示。
        x: 棋子所在的横坐标（从0开始）。
        y: 棋子所在的纵坐标（从0开始）。
        color: 棋子的颜色，取值为"B"或"W"。

    Returns:
        绘制完棋子后的棋盘图像的Numpy数组表示。
    """
    # 定义棋子半径和中心点位置
    piece_radius = 14
    piece_center = (y*32+40, x*32+40)
    # 根据棋子颜色定义圆形的填充颜色
    piece_color = (0, 0, 0) if color == "B" else (255, 255, 255)
    # 在棋盘图像上绘制圆形
    cv2.circle(board_array, piece_center, piece_radius, piece_color, -1)
    return Image.fromarray(board_array)