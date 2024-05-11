#://blog.csdn.net/x2434417239/article/details/111945685
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Mon Dec 28 18:05:17 2020

@author: xiao_gf

"""
import ogr, os

def Extr_Attri(in_shp,outpath,filed_name,file_name): 
    #in_shp为输入shp文件； outpath输出路径；filed_name提取字段的名称；file_name输入文件的名称
    
    shp = ogr.Open(in_shp,1)   #打开shp文件
    lyr = shp.GetLayer()
    lydefn = lyr.GetLayerDefn()
    spatialref = lyr.GetSpatialRef()  #获取空间坐标系
    geomtype = lydefn.GetGeomType()   #文件类型（point，polyline，polygon等）
    a=[]  #初始化列表
    b=[]  #初始化列表
    for i,fea in enumerate(lyr):
        feat = lyr.GetFeature(i)
        fid = feat.GetField(filed_name) 
        a.append(fid)                #获取字段的属性值
    b = list(set(a))                 #剔除重复的属性值，得到属性值列表
    # print(b[1])
    
    for j in range(len(b)):
        
        driver = ogr.GetDriverByName("ESRI Shapefile")   #创建shp驱动
        out_shp = driver.CreateDataSource(outpath+'/'+str(b[j])+file_name+".shp")    #创建文件，文件命名为字段属性值+输入的文件名。
        outlayer = out_shp.CreateLayer(str(b[j])+file_name, srs=spatialref, geom_type=geomtype)
        
        for k in range(0,lydefn.GetFieldCount()):
            fieldDefn = lydefn.GetFieldDefn(k)
            outlayer.CreateField(fieldDefn)
        outlayerDefn = outlayer.GetLayerDefn()
        
        for i in range(0,lyr.GetFeatureCount()):
            feat = lyr.GetFeature(i)
            fid = feat.GetField(filed_name)
            if fid == b[j]:    #判断属性值等于其中某一个值，提取相应的图层
                outFeature = ogr.Feature(outlayerDefn)
                geom = feat.GetGeometryRef()
                outFeature.SetGeometry(geom)
                
                for i in range(0, outlayerDefn.GetFieldCount()):
                    fieldDefn = outlayerDefn.GetFieldDefn(i)
                    
                    outFeature.SetField(outlayerDefn.GetFieldDefn(i).GetNameRef(), feat.GetField(i))
                
                outlayer.CreateFeature(outFeature)
                outFeature = None
        out_shp=None
                
        
if __name__ == "__main__":
    
    filed_name='cityName'
    inpath = r"D:\DATA"
    outpath = r"D:\result\provicial_result"
    
    files = os.listdir(inpath)
    for file in files:
        if file[-4:] == '.shp':
            in_shp_path = os.path.join(inpath,file)
            folder_name = file[:-4]
            if os.path.isdir(outpath):
                os.mkdir(os.path.join(outpath, folder_name))  #创建文件夹
            out_shp_path = os.path.join(outpath, folder_name)
            
            Extr_Attri(in_shp_path,out_shp_path,filed_name,folder_name)
