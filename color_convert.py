import numpy as np
from PIL import Image
from skimage import io

# label_=['forest','grass','farmland','residential','mine','water','road']
# label=[3,4,1,7,6,11,10]
color_map = {
    1: (255, 0, 0),    # 红色  farmland 耕地
    3: (0, 255, 0),    # 绿色  forest 森林
    4: (0, 0, 255),    # 蓝色  grass 草地
    6: (255, 255, 0),  # 黄色  mine  矿山
    7: (255, 0, 255),  # 紫色  residential 居民地
    10: (0, 255, 255), # 青色  road 道路
    11: (128, 128, 128), # 灰色 water 水体
    255: (255,255,255) # 白色  building 建筑物
}

input_path1 = "/mnt/cephfs/zhangww/qingdao0901/2012/2012.tif"
output_path = "/mnt/cephfs/zhangww/qingdao0901/2012/2012.png"
image = io.imread(input_path1, as_gray=True)
h, w = image.shape
output_image = np.zeros((h, w, 3), dtype=np.uint8)
for i in range(h):
    for j in range(w):
        pixel_value = image[i, j]
        if pixel_value in color_map:
            color = color_map[pixel_value]
            output_image[i, j] = color
for i in range(h):
    output_image = Image.fromarray(output_image)
    output_image.save(output_path)