import os
import cv2

def process_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith((".tif", ".png", ".jpg")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # 读取彩色图像
            image = cv2.imread(input_path)
            
            # 将彩色图像转换为灰度图像
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 二值化图像为0-255
            _, binary_image = cv2.threshold(gray_image, 0, 1, cv2.THRESH_BINARY)
            
            # 保存处理后的图像
            cv2.imwrite(output_path, binary_image)

if __name__ == "__main__":
    input_dir = "/mnt/cephfs/share_data/ERM_PAIW_road_512_512/val/labels_color/"
    output_dir = "/mnt/cephfs/share_data/ERM_PAIW_road_512_512/val/labels/"
    # output_dir =  "/mnt/cephfs/zhangww_exper/qingdao_test/painter_output/房屋建筑/building_bn/"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    process_images(input_dir, output_dir)