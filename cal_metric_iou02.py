import os
import cv2

# 定义函数计算两个图像的iou
def calc_iou(img1, img2):
    intersection = cv2.bitwise_and(img1, img2)
    union = cv2.bitwise_or(img1, img2)
    eps = 1e-8
    iou = (cv2.countNonZero(intersection)+eps) / (cv2.countNonZero(union)+eps)
    return iou

# 定义函数计算两个文件夹下所有文件的平均iou
def calc_avg_iou(folder1, folder2):
    # 获取两个文件夹下的所有文件名
    filenames = os.listdir(folder1)
    # 初始化iou总和和文件数
    total_iou = 0
    num_files = len(filenames)
    # 循环遍历所有文件，计算iou并累加总和
    for filename in filenames:
        # 读取文件内容
        img1 = cv2.imread(os.path.join(folder1, filename), cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(os.path.join(folder2, filename), cv2.IMREAD_GRAYSCALE)
        # 计算iou并累加总和
        iou = calc_iou(img1, img2)
        total_iou += iou
        # 打印文件名和iou值
        print(f"{filename}:\t{iou}")
    # 计算平均iou并打印
    avg_iou = total_iou / num_files
    print(f"\nAverage IOU:\t{avg_iou}")

# 两个文件夹的路径
label = "/mnt/cephfs/share_data/building_process/biaozhu/val/labels"
predict = "/mnt/cephfs/data2/other_comper/ali_biaozhu"
print("label path",label)
# 计算平均iou
calc_avg_iou(label, predict)
