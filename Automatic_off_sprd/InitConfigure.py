# -*- coding: UTF-8 -*-
import sys
import os
import Time
import MyString
import xml.etree.ElementTree as ET
from os import path  
import rarfile
import zipfile
import Utilty
import ShowView
import machine
import InitConfigure
class InitConfigure(object):
    """description of class"""

    def __init__(self,patch):
        self.GetConfigure(patch)
        self.patch = patch
    
    def GetConfigure(self,patch):
        keyword_main = {}
        keyword_radio = {}
        keyword_kernel = {}
        time = {}
        directory = {}
        isInitOk = True
        #时间转换的关键字
        key_value = {}
        #是否时间转换
        timeConversion = ""
        targetDirectory = ""
        #第一步初始化，获得开始时间和结束时间和关键词列表
        #获得当前程序所在目录
        #d = path.dirname(__file__)
        #获得配置文件的路径（在打包成exe的时候r"\strings.xml"，改成r"strings.xml"，要不然找不到路径）
        
        #patch = d+r"strings2.xml"
        #print(patch)
        #调试用的路径
        #patch = r"E:\Automatic\strings2.xml"
        '''
        解析xml获得关键字和开始时间和结束时间，和目标文件目录
        '''
        print("开始加载配置文件......")
        try:
            tree = ET.parse(patch)
            root = tree.getroot()
            for child in root:
                #获得标题
                title = child.attrib["title"]
                for sub in child:
                    #判断标题是main还是radio
                    if title == "main":
                        keyword_main[sub.text] = sub.attrib["name"]
                    elif title == "radio":
                        keyword_radio[sub.text] = sub.attrib["name"]
                    elif title == "kernel":
                        keyword_kernel[sub.text] = sub.attrib["name"]
                    elif title == "time":
                        time[sub.attrib["name"]] = sub.text
                    elif title == "targetDirectory":
                        directory[sub.attrib["name"]] = sub.text
                    elif title == "timeConversion":
                        timeConversion = sub.text
                    elif title == "key":
                        key_value[sub.text] = sub.attrib["name"]
        except Exception as e:
            print("配置文件解析错误:",e)
            input('press enter key to exit') 
        #####################################################################

        #第二步把开始时间和结束时间转换成时间戳，并获得当前的年,和目标目录和输出目录
        #获取开始时间和结束时间
        startTime = Time.TimeTransferTimestamp(time["startTime"])
        endTime = Time.TimeTransferTimestamp(time["endTime"])
        #获取当前是哪一年
        year = time["startTime"][0:4]
        #获取目标目录和输出目录
        targetDirectory = directory["target"]
        resultDirectory = directory["result"]
        #目录校验,时间格式校验
        try:
            if not str(targetDirectory).strip() or not str(resultDirectory).strip() or targetDirectory == None or resultDirectory == None:
                print("请检查目标目录和结果目录是否正确")
                isInitOk = False
            if not Time.isTime(time["startTime"]):
                print("请检查开始时间格式是否正确")
                isInitOk = False
            if not Time.isTime(time["endTime"]):
                print("请检查结束时间格式是否正确")
                isInitOk = False
            if not len(key_value) > 0:
                print("请检查key是否正确")
            if not str(timeConversion).strip():
                print("请检查timeConversion是否正确="+str(timeConversion))
        except Exception as e:
            print("配置文件检验错误:",e)
            input('press enter key to exit') 

        self.key_value = key_value
        self.timeConversion = timeConversion
        self.keyword_main = keyword_main
        self.keyword_radio = keyword_radio
        self.keyword_kernel = keyword_kernel
        self.startTime = startTime
        self.endTime = endTime
        self.targetDirectory = targetDirectory
        self.resultDirectory = resultDirectory
        self.year = year
        self.isInitOk = isInitOk
        
        print("配置文件解析完成.....")

    #定义获取参数的函数
    @property
    def _Keyword_main(self):
        return self.keyword_main
    @property
    def _Keyword_radio(self):
        return self.keyword_radio
    @property
    def _Keyword_kernel(self):
        return self.keyword_kernel
    @property
    def _StartTime(self):
        return self.startTime
    @property
    def _EndTime(self):
        return self.endTime
    @property
    def _TargetDirectory(self):
        return self.targetDirectory
    @property
    def _ResultDirectory(self):
        return self.resultDirectory
    @property
    def _Year(self):
        return self.year
    @property
    def _key_value(self):
        return self.key_value
    @property
    def _timeConversion(self):
        return self.timeConversion
    def _isInitOk(self):
        return self.isInitOk



