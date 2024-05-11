import os

# 设置要操作的文件夹路径
folder_path = "/mnt/cephfs/share_data/qingdao_20/infershp/"

# 遍历文件夹下所有文件
for file_name in os.listdir(folder_path):
    # 构建新的文件名
    # new_file_name = file_name[:-4] + file_name[-3:]
    new_file_name = file_name.replace(".tif","")
    
    # 构建旧文件的完整路径
    old_file_path = os.path.join(folder_path, file_name)
    
    # 构建新文件的完整路径
    new_file_path = os.path.join(folder_path, new_file_name)
    
    # 重命名文件
    os.rename(old_file_path, new_file_path)
