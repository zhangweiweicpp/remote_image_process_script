# 将分割图和原图合在一起
from PIL import Image
import matplotlib.pyplot as plt
 
#image1 原图 
#image2 分割图 "/mnt/cephfs/zhangww/qingdao0901/2019-1/final_mask.png"
imgpath1 = "/mnt/cephfs/zhangww/qingdao0901/temppng/2023-1.png"
imgpath2 = "/mnt/cephfs/zhangww/qingdao0901/2023-1/final_mask.png"
outputpath = "/mnt/cephfs/zhangww/qingdao0901/2023-1/" + "merge.png"

image1 = Image.open(imgpath1)
image2 = Image.open(imgpath2)
 
image1 = image1.convert('RGBA')
image2 = image2.convert('RGBA')
 
#两幅图像进行合并时，按公式：blended_img = img1 * (1 – alpha) + img2* alpha 进行
image = Image.blend(image1,image2,0.4)
image.save(outputpath)