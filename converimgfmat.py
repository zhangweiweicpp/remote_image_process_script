from PIL import Image
import os

# 指定文件夹路径
folder_path = '/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/convertdata/labels/'
toext = ".png"

def tif2png(folder_path):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 如果文件是.png文件
        if filename.endswith('.tif'):
            # 构建文件路径
            file_path = os.path.join(folder_path, filename)
            # 打开文件并转换格式
            with Image.open(file_path) as im:
                # 构建新文件名
                new_filename = os.path.splitext(filename)[0] + toext
                # 构建新文件路径
                new_file_path = os.path.join(folder_path, new_filename)
                # 保存文件
                im.save(new_file_path)
            # 删除原始文件
            os.remove(file_path)

if __name__ == "__main__":
    tif2png(folder_path)