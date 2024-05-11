import os
import argparse
from osgeo import gdal

def crop_image(input_path, output_path, crop_size, overlap, ext):
    dataset = gdal.Open(input_path)
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    
    overlap_pixels = int(crop_size * overlap)  # 计算重叠的像素数
    
    for x in range(0, width - crop_size, crop_size - overlap_pixels):
        for y in range(0, height - crop_size, crop_size - overlap_pixels):
            output_filename = os.path.join(output_path, f"{os.path.splitext(os.path.basename(input_path))[0]}_{x}_{y}{ext}")
            gdal.Translate(output_filename, dataset, srcWin=[x, y, crop_size, crop_size], options=['-co', 'ALPHA=NO'])

def batch_crop_images(input_folder, output_folder, crop_size,overlap,ext):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".tif", ".png", ".jpg", ".img")):
            input_path = os.path.join(input_folder, filename)
            crop_image(input_path, output_folder, crop_size,overlap,ext)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, default="/mnt/cephfs/share_data/qingdao_20/oritifval/", help='预测图像的路径，如果没有路径则报错')
    parser.add_argument('--output_dir', type=str, default="/mnt/cephfs/share_data/qingdao_20/qingdaofakev1/val/images/", help='预测图像的路径，如果没有路径则报错')
    parser.add_argument('--crop_size', type=int, default=512, help='裁剪图像的大小，默认为512')
    parser.add_argument('--overlap', type=int, default=0.25, help='重叠率')
    parser.add_argument("--ext",type=str,default=".png",help="裁剪生成的图像格式[.png,.tif,.jpg]")
    args = parser.parse_args()

    if not os.path.exists(args.input_dir):
        raise FileNotFoundError("输入路径不存在！")
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    batch_crop_images(args.input_dir, args.output_dir, args.crop_size, args.overlap,args.ext)
