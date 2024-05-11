import os
import cv2
import numpy as np
from osgeo import gdal

def process_images(input_folder, output_folder, value):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    for filename in os.listdir(input_folder):
        if filename.endswith((".tif", ".png", ".jpg")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            dataset = gdal.Open(input_path, gdal.GA_ReadOnly)
            geotransform = dataset.GetGeoTransform()
            projection = dataset.GetProjection()
            width = dataset.RasterXSize
            height = dataset.RasterYSize
            driver = gdal.GetDriverByName('GTiff')
            out_dataset = driver.Create(output_path, width, height, 1, 1)
            out_dataset.SetProjection(projection)
            out_dataset.SetGeoTransform(geotransform)
            # 读取图像
            image = cv2.imread(input_path,cv2.IMREAD_GRAYSCALE)
            
            # 设置灰度值为2的像素为255，其他像素为0
            result = np.zeros(image.shape, dtype='uint8')
            result[image==value] = 255
            result[image!=value] = 0
            # image[image==value] = 255
            # image[image!=value] = 0
            
            # 保存处理后的图像
            num_bands = 1
            for band in range(1,num_bands+1):
                out_dataset.GetRasterBand(band).WriteArray(result)
            out_dataset = None
            del dataset
            dataset = None
            
            # cv2.imwrite(output_path, image)
            # cv2.imwrite(output_path, result)


if __name__ == "__main__":
    input_folder = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/temp/"
    output_folder = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/out/"
    value = 255
    process_images(input_folder, output_folder, value)
