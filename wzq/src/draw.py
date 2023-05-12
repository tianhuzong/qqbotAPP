from PIL import Image
import numpy as np
import cv2

def draw_piece(board_array, x, y, color):
    """������ͼ���ϻ������ӡ�

    Args:
        board_array: ����ͼ���Numpy�����ʾ��
        x: �������ڵĺ����꣨��0��ʼ����
        y: �������ڵ������꣨��0��ʼ����
        color: ���ӵ���ɫ��ȡֵΪ"B"��"W"��

    Returns:
        ���������Ӻ������ͼ���Numpy�����ʾ��
    """
    # �������Ӱ뾶�����ĵ�λ��
    piece_radius = 14
    piece_center = (y*32+40, x*32+40)
    # ����������ɫ����Բ�ε������ɫ
    piece_color = (0, 0, 0) if color == "B" else (255, 255, 255)
    # ������ͼ���ϻ���Բ��
    cv2.circle(board_array, piece_center, piece_radius, piece_color, -1)
    return Image.fromarray(board_array)