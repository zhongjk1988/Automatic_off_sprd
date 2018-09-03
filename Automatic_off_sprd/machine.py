# -*- coding: UTF-8 -*-
import sys
import FileUtilty
import os
import Time
import MyString
import xml.etree.ElementTree as ET
from os import path  
import rarfile
import zipfile
import Utilty
import ShowView
import kernel

class Machine(object):
    """description of class"""
    
    def __init__(self, init):
        self.init = init

    def pringss(self):
        print(self.key_dict)
        
    def getMainResult(self,init):
        print("解压获取文件完成......")
        print("开始解析main log.....")
        #第三获得目标目录下的所有main log和时间戳的字典
        filenames_main = FileUtilty.getTargetFileTimeList(init.targetDirectory,"main",init.year)
        #第四根据时间戳和main log文件的字典获得目标文件的列表
        filenames_main = MyString.getTargetfilename(filenames_main,init.startTime,init.endTime)
        print(filenames_main)
        #按时间先后给文件列表排序
        filenames_main.sort()
        #打印索引到的文件名
        #print (filenames_main)
        #第五开始统计需要的数据并打印需要打印的内容
        mainResult = FileUtilty.readMainFiles(filenames_main,init.startTime,init.endTime,init.keyword_main,init.year,init.resultDirectory)
        print("main log解析完成.....")
        return mainResult
        
    def getRadioResult(self,init):
        print("开始解析radio log.....")
        #第三获得目标目录下的所有radio log和时间戳的字典
        filenames_radio = FileUtilty.getTargetFileTimeList(init.targetDirectory,"radio",init.year)
        #第四根据时间戳和radio log文件的字典获得目标文件的列表
        filenames_radio = MyString.getTargetfilename(filenames_radio,init.startTime,init.endTime)
        #按时间先后给文件列表排序
        filenames_radio.sort()
        #第五开始统计需要的数据并打印需要打印的内容
        radioResult = FileUtilty.readRadioFiles(filenames_radio,init.startTime,init.endTime,init.keyword_radio,init.year,init.resultDirectory)
        #print(radioResult)
        print("radio log解析完成.....")
        return radioResult


    def getKernelResult(self,init):
        print("开始解析kernel log.....")
        #第三获得目标目录下的所有kernel log和时间戳的字典
        filenames_kernel = FileUtilty.getTargetFileTimeList(init.targetDirectory,"kernel",init.year)
        #第四根据时间戳和kernel log文件的字典获得目标文件的列表
        filenames_kernel = MyString.getTargetfilename(filenames_kernel,init.startTime,init.endTime)
        #按时间先后给文件列表排序
        print(filenames_kernel)
        print(init.timeConversion)
        print(init.key_value)
        for path_log in filenames_kernel:
            #已slog为标志过滤掉展讯的log
            if not "slog" in path_log:
                #把文件名改为txt作为结果文件
                result_path = os.path.splitext(path_log)[0]+".txt"
                kernel.timeConversion(path_log,result_path,init.key_value)
        filenames_kernel.sort()
        #第五开始统计需要的数据并打印需要打印的内容
        kernelResult = FileUtilty.readKernelFiles(filenames_kernel,init.startTime,init.endTime,init.keyword_kernel,init.year,init.resultDirectory)
        #print(radioResult)
        print("kernel log解析完成.....")
        return kernelResult

    def getResult(self):
        result = {}
        mainResult = self.getMainResult(self.init)
        radioResult = self.getRadioResult(self.init)
        kernelResult = self.getKernelResult(self.init)
        if kernelResult:
            for key,address in kernelResult.items():
                if "mainData" in mainResult.keys():
                    mainResult["mainData"][key] = address
        if mainResult:
            for key,address in mainResult.items():
                print("mainResult log....."+key)
                result[key] = address
        if radioResult:
            for key,address in radioResult.items():
                result[key] = address
        return result