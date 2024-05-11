#!/usr/bin/python3.8
# -*- coding: utf-8 -*-  
#背景 - 1，建筑 - 2，道路 - 3，水 - 4，贫瘠 - 5，森林 - 6，农业 - 7。无数据区域分配为 0，应忽略。
#target:  背景 - 0，建筑 - 8，道路 - 10，水 - 11，贫瘠 - 1，森林 - 3，农业 - 1。无数据区域分配为 0，应忽略。
import cv2
import os

def main():
    path='train/masks/'
    files=os.listdir(path)
    i=0
    for file_name  in files:
        img =cv2.imread(path+file_name,-1)
        row,col=img.shape
        for m in range(row):
            for n in range(col):
                val=img[m][n]
                if val==1:
                    img[m][n]=0
                elif val==2:
                    img[m][n]=8
                elif  val==3:
                    img[m][n]=10
                elif val==4:
                    img[m][n]=11
                elif val==5:
                    img[m][n]=1
                elif val==6:
                    img[m][n]=3
                elif val ==7:
                    img[m][n]=1
                else:
                    img[m][n]=0
        cv2.imwrite(path+file_name,img)
    

        i=i+1
        print(i)




if __name__ == "__main__":
   main()