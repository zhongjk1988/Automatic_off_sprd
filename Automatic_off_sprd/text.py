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
import machine
import InitConfigure
  
myInit = InitConfigure.InitConfigure()
print("初始化检验完成.....")

#判断配置文件是否加载成功
if myInit._isInitOk:
    '''
    第三解压目标文件下的压缩文件
    '''
    FileUtilty.GetReady(myInit)
    print("解压获取文件完成......")
    print("开始解析modem log.....")
    
else:
    print("加载配置文件错误...")
    pass

mainMachine = machine.Machine(myInit)
result = mainMachine.getResult()
if result:
    ShowView.showMianInfo(result)
'''
radioMachine = machine.Machine(keyword_radio,year,targetDirectory,resultDirectory,startTime,endTime)
result = radioMachine.getRadioResult()
print("=============",result)
radioMachine = machine.Machine(keyword_kernel,year,targetDirectory,resultDirectory,startTime,endTime)
result = radioMachine.getKernelResult()
print("=============",result)
'''