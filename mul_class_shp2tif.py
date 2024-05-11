from osgeo import gdal, ogr, osr
import os

def RasterzeTheVectorToRasterr(temp_shp_path="/mnt/cephfs/zhangww/testdata/秦岭三调-阿里(1)/sandiao_AIESEG_1_6144_27648_512_512/temp.shp"):
    # 参数说明： 输出的栅格数据，注意该数据必须以update模式打开、指定要更新的波段个数(更新123波段)、指定的图层、几何图形坐标转换图像行列号函数、几何图形坐标转换图像行列号参数、以及图层中属性字段属性值
    inputfilePath="/mnt/cephfs/zhangww/testdata/秦岭三调-阿里(1)/sandiao_AIESEG_1_6144_27648_512_512/181989168-1703586621214-2790080.shp"
    outputfile="/mnt/cephfs/zhangww/testdata/秦岭三调-阿里(1)/sandiao_AIESEG_1_6144_27648_512_512/aa.tif"
    templetefile="/mnt/cephfs/zhangww/testdata/huangdao_Clip.tif"
    data = gdal.Open(templetefile)
    x_res = 512
    y_res = 512
    vector = ogr.Open(inputfilePath)
    # 创建一个新的内存数据源，并将只读数据源中的内容复制到新数据源
    driver = ogr.GetDriverByName('ESRI Shapefile')
    writable_datasource = driver.CreateDataSource(temp_shp_path)  # 创建空的可写数据源
    writable_datasource.CopyLayer(vector.GetLayer(), 'new_layer')  # 复制只读数据源中的图层到可写数据源
    # 获取可写数据源中的图层
    write_layer = writable_datasource.GetLayer('new_layer')

    layer = vector.GetLayer()
    targetDataSet = gdal.GetDriverByName('GTiff').Create(outputfile, x_res, y_res, 1, gdal.GDT_Byte)
    # targetDataSet=gdal.GetDriverByName('GTiff').CreateCopy(templetefile,data)
    targetDataSet.SetGeoTransform(data.GetGeoTransform())
    targetDataSet.SetProjection(data.GetProjection())
    # band = targetDataSet.GetRasterBand(1)
    # NoData_value = -999
    # band.SetNoDataValue(NoData_value)
    # band.FlushCache()

    cg_pixvalue = {"草地": 0, "道路": 10,"房屋建筑": 7,"林地": 3,"硬化地表": 0,"种植土地": 1,"游泳池": 0,"水域": 11}
    feature_num= layer.GetFeatureCount()

    print("feature_num02:",feature_num)
    for i in range(feature_num):
        feature = layer.GetFeature(i)  # access the feature by its index
        geometry  = feature.GetGeometryRef()
        # 获取原来的category属性值
        # 检查是否是多边形
        if geometry.GetGeometryType() == ogr.wkbPolygon:
            print('Feature', i, 'is a polygon.')
        else:
            print('Feature', i, 'is not a polygon.')
        category = feature.GetField('category')
        print("category",category)

        # 根据映射关系将属性值替换为对应的属性
        category_value = cg_pixvalue.get(category, 255)
        feature.SetField("category", category_value)
        print("category_value:",category_value)
        # 更新feature
        write_layer.SetFeature(feature)
    """
            gdal_rasterize [--help] [--help-general]
        [-b <band>]... [-i] [-at]
        [-oo <NAME>=<VALUE>]...
        {[-burn <value>]... | [-a <attribute_name>] | [-3d]} [-add]
        [-l <layername>]... [-where <expression>] [-sql <select_statement>|@<filename>]
        [-dialect <dialect>] [-of <format>] [-a_srs <srs_def>] [-to <NAME>=<VALUE>]...
        [-co <NAME>=<VALUE>]... [-a_nodata <value>] [-init <value>]...
        [-te <xmin> <ymin> <xmax> <ymax>] [-tr <xres> <yres>] [-tap] [-ts <width> <height>]
        [-ot {Byte/Int8/Int16/UInt16/UInt32/Int32/UInt64/Int64/Float32/Float64/
            CInt16/CInt32/CFloat32/CFloat64}] [-optim {AUTO|VECTOR|RASTER}] [-q]
        <src_datasource> <dst_filename>
    """
    gdal.RasterizeLayer(targetDataSet, [1], write_layer, options=["ATTRIBUTE=Value"])
    writable_datasource = None

def shp_to_tif_using_ref(input_path, output_path):
    # Load Shapefile
    shp_ds = ogr.Open(input_path)

    # Fetch each feature from input shapefile, and add them to mem_layer
    shp_layer = shp_ds.GetLayer()
    shp_layer.ResetReading()

    #  Create a new datasource in memory
    mem_ds = ogr.GetDriverByName('Memory').CreateDataSource('out')
    mem_layer = mem_ds.CreateLayer('polygonized raster', geom_type=ogr.wkbPolygon)

    # Add a new field
    field_defn = ogr.FieldDefn('category', ogr.OFTString)
    mem_layer.CreateField(field_defn)

    cg_pixvalue = {"草地": 0, "道路": 10,"房屋建筑": 7,"林地": 3,"硬化地表": 0,"种植土地": 1,"游泳池": 0,"水域": 11}

    for feature in shp_layer:
        # 获取原来的category属性值
        category_value = feature.GetField('category')

        # 根据映射关系将属性值替换为对应的属性
        new_category_value = cg_pixvalue.get(category_value, 255)
        feature.SetField('category', new_category_value)

        # 更新feature
        mem_layer.SetFeature(feature)

    shp_layer.ResetReading()

    x_res = 512
    y_res = 512

    # Create GeoTIFF file
    output_ds = gdal.GetDriverByName('GTiff').Create(output_path, x_res, y_res, 1, gdal.GDT_Byte)
    # 目标band 1
    band = output_ds.GetRasterBand(1)
    # 白色背景
    #NoData_value = -999
    NoData_value = 0
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    # Dictionary of pixel values
    # cg_pixvalue = {"草地": 255, "道路": 10,"房屋建筑": 7,"林地": 3,"硬化地表": 0,"种植土地": 1,"游泳池": 0,"水域": 11}
    # for category, pix_val in cg_pixvalue.items():
    gdal.RasterizeLayer(output_ds, [1], mem_layer, options=["ATTRIBUTE=category"])#our
    # gdal.RasterizeLayer(output_ds, [1], shp_layer, None, None, [pix_val], options=["ALL_TOUCHED="+"False"])
        
    # Close datasets
    output_ds = None
    shp_ds = None
    mem_ds = None


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
# shp_to_tif_using_ref(input_path, output_path)

RasterzeTheVectorToRasterr()