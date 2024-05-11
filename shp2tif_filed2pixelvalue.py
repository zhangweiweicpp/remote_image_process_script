from osgeo import gdal, ogr, osr
import os

def shp_to_tif_using_ref(input_path, output_path):
    # Load Shapefile
    shp_ds = ogr.Open(input_path)

    x_res = 512
    y_res = 512

    tmp_output_path = output_path.replace(".png", ".tif")  # temporary output path for GeoTIFF
    # Configure the output raster
    geotransform = (0, 1, 0, 0, 0, 1)
    out_srs = osr.SpatialReference().ImportFromEPSG(4326)  # WGS84 coordinate system
    # Create GeoTIFF file
    target_ds = gdal.GetDriverByName('GTiff').Create(tmp_output_path, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform(geotransform)
    target_ds.SetProjection(out_srs.ExportToWkt())
    # Dictionary of pixel values
    cg_pixvalue = {"草地":255, "道路":10,"房屋建筑":7,"林地":3,"硬化地表":0,"种植土地":1,"游泳池":0,"水域":11}
    no_data_value = -9999
    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(no_data_value)
    band.FlushCache()
    for category, pix_val in cg_pixvalue.items():
        
        shp_lyr = shp_ds.GetLayer(0)  # Get the first layer
        shp_lyr.ResetReading()   #IMPORTANT: Reset reading
        shp_lyr.SetAttributeFilter(f"category = '{category}'")  # Set attribute filter for each category
        gdal.RasterizeLayer(target_ds, [1], shp_lyr, burn_values=[pix_val])

    #close GeoTIFF
    target_ds = None

    # Translate GeoTIFF to PNG
    gdal.Translate(output_path, tmp_output_path, format='PNG')

    #remove temporary GeoTIFF
    # os.remove(tmp_output_path)


# 使用示例
# input_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/181989168-1703572376635-6314947.shp"
# ref_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/reference_img/2019origin_cut.tif"
# output_path = "/mnt/cephfs/qingling_png2tif/建筑物评测/阿里结果/建筑物提取/181989168-1703572376635-6314947.tif"
# shp_to_tif_using_ref(input_path, ref_path, output_path)

input_path = "/mnt/cephfs/zhangww/testdata/秦岭三调-阿里(1)/sandiao_AIESEG_1_6144_27648_512_512/181989168-1703586621214-2790080.shp"
output_folder = "/mnt/cephfs/zhangww/testdata/秦岭三调-阿里(1)/sandiao_AIESEG_1_6144_27648_512_512/"
# ref_folder = "/mnt/cephfs/share_data/qingdao_20/oritif/"#原图tif路径

# for file in os.listdir(input_folder):
file = os.path.basename(input_path)
file_name,_ = os.path.splitext(file)
# input_path = os.path.join(input_folder,file_name+".shp")
output_path = os.path.join(output_folder,file_name+".png")
# ref_path = os.path.join(ref_folder,file_name+".tif")
print(input_path)
print(output_path)
# print(ref_path)
shp_to_tif_using_ref(input_path, output_path)