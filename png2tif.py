from osgeo import gdal, osr
import os

#single
# def png_to_tif_with_ref(input_path, ref_path, output_path):
#     ref_raster = gdal.Open(ref_path)
#     geotransform = ref_raster.GetGeoTransform()
#     projection = ref_raster.GetProjection()

#     input_raster = gdal.Open(input_path)
#     driver = gdal.GetDriverByName('GTiff')
#     output_raster = driver.CreateCopy(output_path, input_raster, 0)

#     output_raster.SetGeoTransform(geotransform)
#     output_raster.SetProjection(projection)
#     output_raster = None

#multil
def png_to_tif_with_ref(input_dir, ref_path, output_dir):
    ref_raster = gdal.Open(ref_path)
    geotransform = ref_raster.GetGeoTransform()
    projection = ref_raster.GetProjection()

    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.png', '.tif'))

            input_raster = gdal.Open(input_path)
            driver = gdal.GetDriverByName('GTiff')
            output_raster = driver.CreateCopy(output_path, input_raster, 0)

            output_raster.SetGeoTransform(geotransform)
            output_raster.SetProjection(projection)
            output_raster = None
            print(f"Converted {filename} to TIFF")

# 使用示例
input_path = "/mnt/cephfs/qingling_png2tif/input/"
ref_path = "/mnt/cephfs/qingling_png2tif/front.tif"
output_path = "/mnt/cephfs/qingling_png2tif/output/"
png_to_tif_with_ref(input_path, ref_path, output_path)