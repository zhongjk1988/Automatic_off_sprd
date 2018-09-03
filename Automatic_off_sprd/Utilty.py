
# -*- coding: UTF-8 -*-
import sys
import os
import rarfile
import zipfile
import tarfile
import MyString
import Time
from collections import Counter
'''
解压rar文件，只能解压windows压缩的，解压不了好压的
'''
def un_rar(file_name):
    """unrar zip file"""
    filePath = file_name.split(".")[0]
    rar = rarfile.RarFile(file_name)
    #if os.path.isdir(file_name + "_files"):
    if os.path.isdir(filePath):
        pass
    else:
        #os.mkdir(file_name + "_files")
        os.mkdir(filePath)

    rar.extractall(r'E:\a')
    rar.close()

'''
解压zip文件，只能解压windows压缩的，解压不了好压的
'''
def un_zip(file_name):
    """unzip zip file"""
    zip_file = zipfile.ZipFile(file_name)
    filePath = file_name.split(".")[0]
    #if os.path.isdir(file_name + "_files"):
    if os.path.isdir(filePath):
        pass
    else:
        #os.mkdir(file_name + "_files")
        os.mkdir(filePath)
    for names in zip_file.namelist():
        #zip_file.extract(names,file_name + "_files")
        zip_file.extract(names,filePath)
    zip_file.close()

'''
解压tar文件，只能解压windows压缩的，解压不了好压的
'''
def un_tar(file_name):
    """untar zip file"""
    tar = tarfile.open(file_name)
    filePath = file_name.split(".")[0]
    #取“Folder_”关键之加后8位的前面的路径
    index = filePath.find(r"Folder_") + len(r"Folder_") + 8
    filePath = filePath[:index]
    names = tar.getnames()
    #if os.path.isdir(file_name + "_files"):
    if os.path.isdir(filePath):
        pass
    else:
        #os.mkdir(file_name + "_files")
        os.mkdir(filePath)
    #因为解压后是很多文件，预先建立同名目录
    for name in names:
        #tar.extract(name, file_name + "_files/")
        tar.extract(name, filePath)
    tar.close()

'''
'''
def getRRCTIme(data):
    result = {}
    counter = []
    for i in data:
        #count 搜索字符串在列表中出现的次数
        if not i in counter and not i == 0:
            if data.count(i) >= 1:
                if int(i) < 60:
                    if r"<1M" in result.keys():
                        result["<1M"] = result["<1M"] + data.count(i)
                    else:
                        result["<1M"] = data.count(i)
                elif int(i) >= 60 and int(i) <= 5*60:
                    if r"1M~5M" in result.keys():
                        result["1M~5M"] = result["1M~5M"] + data.count(i)
                    else:
                        result["1M~5M"] = data.count(i)
                elif int(i) >= 5*60 and int(i) <= 10*60:
                    if r"5M~10M" in result.keys():
                        result["5M~10M"] = result["5M~10M"] + data.count(i)
                        print(str(i)+">>>"+str(data.count(i)))
                    else:
                        result["5M~10M"] = data.count(i)
                elif int(i) > 10*60 and int(i) <= 20*60:
                    if r"10M~20M" in result.keys():
                        result["10M~20M"] = result["10M~20M"] + data.count(i)
                    else:
                        result["10M~20M"] = data.count(i)
                elif int(i) > 20*60 and int(i) <= 30*60:
                    if r"20M~30M" in result.keys():
                        result["20M~30M"] = result["20M~30M"] + data.count(i)
                    else:
                        result["20M~30M"] = data.count(i)
                elif int(i) > 30*60 and int(i) <= 40*60:
                    if r"30M~40M" in result.keys():
                        result["30M~40M"] = result["30M~40M"] + data.count(i)
                    else:
                        result["30M~40M"] = data.count(i)
                elif int(i) > 40*60 and int(i) <= 50*60:
                    if r"40M~50M" in result.keys():
                        result["40M~50M"] = result["40M~50M"] + data.count(i)
                    else:
                        result["40M~50M"] = data.count(i)
                elif int(i) > 50*60:
                    if r">50M" in result.keys():
                        result[">50M"] = result[">50M"] + data.count(i)
                    else:
                        result[">50M"] = data.count(i)
            counter.append(i)
                
    return result


def getDataRadioTechnology(data):
    result = {}
    counter = []
    for i in data:
        #count 搜索字符串在列表中出现的次数
        if not i in counter:
            if data.count(i) >= 1:
                result[i] = data.count(i)
    return result

def getNetworkMode(value):
    if value == 0:
        return "UNKNOWN"
    elif value == 1:
        return "GPRS"
    elif value == 2:
        return "EDGE"
    elif value == 3:
        return "UMTS"
    elif value == 4:
        return "IS95A"
    elif value == 5:
        return "IS95B"
    elif value == 6:
        return "1xRTT"
    elif value == 7:
        return "EVDO_0"
    elif value == 8:
        return "EVDO_A"
    elif value == 9:
        return "HSDPA"
    elif value == 10:
        return "HSUPA"
    elif value == 11:
        return "HSPA"
    elif value == 12:
        return "EVDO_B"
    elif value == 13:
        return "EHRPD"
    elif value == 14:
        return "LTE"
    elif value == 15:
        return "HSPAP"
    elif value == 16:
        return "GSM"
    elif value == 17:
        return "SCDMA"
    elif value == 18:
        return "IWLAN"
    elif value == 19:
        return "LTE_CA"

def getNetworkValue(value):
    if value == "UNKNOWN":
        return 0
    elif value == "GPRS":
        return 1
    elif value == "EDGE":
        return 2
    elif value == "UMTS":
        return 3
    elif value == "IS95A":
        return 4
    elif value == "IS95B":
        return 5
    elif value == "1xRTT":
        return 6
    elif value == "EVDO_0":
        return 7
    elif value == "EVDO_A":
        return 8
    elif value == "HSDPA":
        return 9
    elif value == "HSUPA":
        return 10
    elif value == "HSPA":
        return 11
    elif value == "EVDO_B":
        return 12
    elif value == "EHRPD":
        return 13
    elif value == "LTE":
        return 14
    elif value == "HSPAP":
        return 15
    elif value == "GSM":
        return 16
    elif value == "SCDMA":
        return 17
    elif value == "IWLAN":
        return 18
    elif value == "LTE_CA":
        return 19



def isWakeUpCpu(flags):
    if (flags & 0x00000001) or (flags & 0x00000006) or (flags & 0x0000000a) or (flags & 0x0000001a):
        return True
    return False

def getWakeLockInfo(line):
    #获取锁的名字,并去掉前后的"号
    tag = MyString.getIndexCher(line,",",2,"tag=").strip("\"")
    #获取lock值
    lock = MyString.getIndexCher(line,",",0,"lock=")
    return tag,lock

def getSensorInfo(line):
    sensorStutas = MyString.getIndexCher(str(line,encoding='utf-8'),",",1,"enable=").strip("\n")
    sensorsName = MyString.getIndexCher(line,",",0,"activate sensors").strip("\"")
    return sensorStutas,sensorsName

def getGlobalInfo(line):
    #获取设备名，wifi/bluetooth_on/mobile_data
    globalName = MyString.getIndexCher(line,",",0,"name=").strip("\n")
    #获取状态值先按","切割取第二个值，然后再按" "切割取value=后面的值 #状态1 代表开启 0代表关闭
    value = line.split(",")[1]
    value = MyString.getIndexCher(value," ",1,"value=").strip("\n")
    return globalName,value


def calculation_All_Time_Current(startTime,all_Time,endTime,fd_main,strTitle,year):
    if Time.isTime(startTime) and int(Time.TimeTransferTimestamp(str(startTime))) > 0:
        fd_main.writelines(strTitle+str(all_Time+Time.DuractionTime(year,startTime,Time.TimeTimestampTransfer(endTime)))+"秒"+"\n")
        startTime = 0
    else:
        fd_main.writelines(strTitle+str(all_Time)+"秒"+"\n")
        startTime = 0
    return startTime

def addWakeLockToDeque(lockName,totalityLockDeque,time):
    if lockName in totalityLockDeque.keys():
        totalityLockDeque[lockName][0] = totalityLockDeque[lockName][0] + 1
        totalityLockDeque[lockName][1] = totalityLockDeque[lockName][1] + time
    else:
        totalityLockDeque[lockName] = [1,time]
    return totalityLockDeque


def isInLockDeque(differenceLock,tag,lock,diffTime):
    for index,wakeLock in enumerate(differenceLock):
        if str(wakeLock._lock_) == lock and str(wakeLock._name_) == tag and str(wakeLock._time_) == diffTime:
            print("重复打印的锁:"+ "时间:"+diffTime+"lock=" + lock +"tag="+tag)
            return True
    return False