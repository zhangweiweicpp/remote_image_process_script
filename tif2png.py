import os
from PIL import Image
from osgeo import gdal
import cv2

# 指定文件夹路径
input_folder  = "/mnt/cephfs/zhangww/qingdao0901/qingdao_weixing_20230829"
output_folder = "/mnt/cephfs/zhangww/qingdao0901/temppng/"

for filename in os.listdir(input_folder):
    if filename.endswith(".tif"):
        # 构造输入文件的完整路径
        input_path = os.path.join(input_folder, filename)
        
        # 构造输出文件的完整路径
        output_filename = os.path.splitext(filename)[0] + ".png"
        output_path = os.path.join(output_folder, output_filename)
        
        # 使用OpenCV加载tif文件
        image = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        
        # 将图像保存为png格式
        cv2.imwrite(output_path, image)