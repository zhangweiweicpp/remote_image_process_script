from osgeo import gdal, ogr, osr
import os
# 提法2 shp https://blog.csdn.net/Prince999999/article/details/105822718


def shp_to_tif_using_ref(input_path, ref_path, output_path):
    # Load Shapefile
    shp_ds = ogr.Open(input_path)
    shp_lyr = shp_ds.GetLayer()

    # Load reference TIFF
    ref_ds = gdal.Open(ref_path)

    # Get parameters from reference TIFF
    geotransform = ref_ds.GetGeoTransform()
    projection = ref_ds.GetProjection()
    band = ref_ds.GetRasterBand(1)
    x_res = ref_ds.RasterXSize
    y_res = ref_ds.RasterYSize

    # Create TIFF file
    target_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, 1, band.DataType)
    target_ds.SetGeoTransform(geotransform)
    target_ds.SetProjection(projection)

    # Rasterize using values from 'value' attribute in Shapefile
    # gdal.RasterizeLayer(target_ds, [1], shp_lyr, options=["ATTRIBUTE=value"])#our
    gdal.RasterizeLayer(target_ds, [1], shp_lyr, burn_values=[255])#


# 使用示例
# input_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/181989168-1703572376635-6314947.shp"
# ref_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/reference_img/2019origin_cut.tif"
# output_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/181989168-1703572376635-6314947.tif"
# shp_to_tif_using_ref(input_path, ref_path, output_path)

input_folder = "/mnt/cephfs/share_data/qingdao_20/infershp/"
output_folder = "/mnt/cephfs/share_data/qingdao_20/label/"
ref_folder = "/mnt/cephfs/share_data/qingdao_20/oritif/"#原图tif路径
for file in os.listdir(ref_folder):
    file_name,_ = os.path.splitext(file)
    input_path = os.path.join(input_folder,file_name+".shp")
    output_path = os.path.join(output_folder,file_name+".tif")
    ref_path = os.path.join(ref_folder,file_name+".tif")
    print(input_path)
    print(output_path)
    print(ref_path)
    shp_to_tif_using_ref(input_path, ref_path, output_path)
