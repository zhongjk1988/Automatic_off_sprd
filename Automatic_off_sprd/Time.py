#!/usr/bin/env python
# encoding: utf-8
import time
import datetime
import re
import MyString

#时间转换成时间戳
def TimeTransferTimestamp(dt):
    #dt = "2016-05-05 20:28:54"
    #转换成时间数组
    dt = dt.replace("_"," ") #把时间里面的下划线改为空格
    myTime = ""
    #过滤掉字符串里面除了'0123456789-: '之外的字符
    dt = filter(lambda ch: ch in '0123456789-: ', dt)
    #列表中的所有值转换为字符串，以及列表拼接成一个字符串
    for i in dt:
        myTime = myTime + i
    if str(myTime).count("-") > 2:
        myTime = MyString.replace(myTime,13,16,":")
    timeArray = time.strptime(str(myTime), "%Y-%m-%d %H:%M:%S")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp

#转换成新的时间格式
def TimeFormatConversiondt(dt):
    #dt = "2016-05-05 20:28:54"
    #转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #转换成新的时间格式(20160505-20:28:54)
    dt_new = time.strftime("%Y%m%d-%H:%M:%S",timeArray)
    print ("dt_new=",dt_new)
    return dt_new

#时间戳转换成时间
def TimeTimestampTransfer(timestamp):
    #timestamp = 1462451334
    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
    #print ("dt",dt)
    return dt

#获取当前时间并按指定的格式转换 format "%Y-%m-%d %H:%M:%S"
def GetLocalTime(format):
    #获取当前时间
    time_now = int(time.time())
    #转换成localtime
    time_local = time.localtime(time_now)
    #转换成新的时间格式(2016-05-09 18:59:20)
    dt = time.strftime(format,time_local)
    print ("dt",dt)
    return dt

def inTheTime(startTime,endTime,currentTime):
     #判断获取的是否是时间
     if(currentTime.count("-")== 2 and currentTime.count(":")== 2):
        #把时间转换成时间戳
        currentTime = TimeTransferTimestamp(currentTime)
        #判断时间是否在时间段内
        if(currentTime >= startTime and currentTime <= endTime):
            return True
        else:
            return False
     else:
        return False

def DuractionTime(year,startTime,endTime):
    if(str(startTime).count("-")== 2 and str(startTime).count(":")== 2 and str(endTime).count("-")== 2 and str(endTime).count(":")== 2):
        #把时间转换成时间戳
        #print("startTime="+str(startTime)+">>"+"endTime="+str(endTime))
        startTime = TimeTransferTimestamp(startTime)
        endTime = TimeTransferTimestamp(endTime)
        #print(str(endTime - startTime))
        #返回时间戳的差值，单位是秒
        return endTime - startTime
    return 0 

def isTime(currentTime):
    if(str(currentTime).count("-")== 2 and str(currentTime).count(":")== 2):
        return True
    return False



if __name__ == '__main__':
    print("time_self")