import cv2
import os
import numpy as np

# 指定文件夹 路径
folder_path = '/opt/AI_Algorithm/Painter/datasets/ade20k/annotations_with_color/training'

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 如果文件是二值图
    if filename.endswith('.png') or filename.endswith('.jpg'):
        # 构建文件路径
        file_path = os.path.join(folder_path, filename)
        # 打开文件并转换为黑白的RGB图
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        img_bw = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
        img_bw[img == 255] = [255, 255, 255]   # 白色像素替换为黑色像素
        img_bw[img == 0] = [0, 0, 0]   # 黑色像素替换为灰色像素
        # 构建新文件名
        new_filename = os.path.splitext(filename)[0] + '_color.jpg'
        # 构建新文件路径
        new_file_path = os.path.join(folder_path, new_filename)
        # 保存文件
        cv2.imwrite(new_file_path, img_bw)

