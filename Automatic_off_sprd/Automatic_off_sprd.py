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
import PygalShow
  
def main():

    try:
        patch = os.path.realpath(__file__)
        patch = os.path.dirname(patch)+"\strings2.xml"
        print('path:', patch)
        #myInit = InitConfigure.InitConfigure(patch)
        myInit = InitConfigure.InitConfigure("E:\Automatic\strings2.xml")
    except Exception as e:
        print("初始化检验失败:",e)
        input('press enter key to exit') 
        
    #判断配置文件是否加载成功
    try:
        if myInit._isInitOk:
            '''
            第三解压目标文件下的压缩文件
            '''
            FileUtilty.GetReady(myInit)
            print("解压获取文件完成......")
            print("开始解析modem log.....")
        else:
            print("加载配置文件失败...")
            pass
    except Exception as e:
        print("加载配置文件错误:",e)
        input('press enter key to exit') 

    mainMachine = machine.Machine(myInit)

    result = mainMachine.getResult()
    try:
        if result:
            pygalShow = PygalShow.PygalShow(result,myInit.targetDirectory)
            pygalShow.show()
            #ShowView.showMianInfo(result)
    except Exception as e:
        print("展示结果失败:",e)
        input('press enter key to exit') 

if __name__ == "__main__":
    main()
    input('press enter key to exit') 


