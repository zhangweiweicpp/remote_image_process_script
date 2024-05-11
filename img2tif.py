import os
from osgeo import gdal

def convert_img_to_tif(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".img"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".tif")

            # 打开.img文件
            dataset = gdal.Open(input_path)

            # 转换为.tif格式
            gdal.Translate(output_path, dataset, format="GTiff")

            dataset = None

if __name__ == "__main__":
    input_folder = "/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/"
    output_folder = "/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/"

    convert_img_to_tif(input_folder, output_folder)
