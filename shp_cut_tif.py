from osgeo import gdal

def clip_image(input_tif, input_shp, output_tif):
    # 打开.tif文件
    src_ds = gdal.Open(input_tif)

    # 设置裁剪区域
    options = gdal.WarpOptions(cutlineDSName=input_shp, cropToCutline=True)

    # 执行裁剪
    gdal.Warp(output_tif, src_ds, options=options)

    print("裁剪完成，结果保存为：" + output_tif)

# 输入文件路径
input_tif = '/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/convertdata/res/Merge.tif'  # 替换为输入.tif文件的路径
input_shp = '/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/convertdata/shp/Converted_Graphics_3.shp'  # 替换为输入.shp文件的路径
output_tif = '/mnt/cephfs/zhangww_exper/qingdao_test/非耕地/convertdata/Merge_cuttest.tif'  # 替换为输出.tif文件的路径

# 裁剪图像并保存
clip_image(input_tif, input_shp, output_tif)