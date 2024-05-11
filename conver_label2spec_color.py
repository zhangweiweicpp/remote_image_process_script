import os
import cv2

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".tif", ".png", ".jpg")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # 读取图像
            image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
            
            # 设置灰度值为2的像素为255，其他像素为0
            image[image != 0 ] = 255
            image[image == 0] = 0
            
            # 保存处理后的图像
            cv2.imwrite(output_path, image)

if __name__ == "__main__":
    input_folder = "/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/dlinknet_output/temp/"
    output_folder = "/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/dlinknet_output/result/"
    
    process_images(input_folder, output_folder)
