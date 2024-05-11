from PIL import Image

def resize_tif_image(input_path, output_path, size):
    image = Image.open(input_path)
    resized_image = image.resize(size)
    resized_image.save(output_path)

# 示例用法
input_path = "/mnt/cephfs/qingling_png2tif/resize/房屋建筑.tif"
output_path = "/mnt/cephfs/qingling_png2tif/resize/房屋建筑resize.tif"
size = (2814, 2060)  # 要resize的大小，可以根据需要调整
resize_tif_image(input_path, output_path, size)