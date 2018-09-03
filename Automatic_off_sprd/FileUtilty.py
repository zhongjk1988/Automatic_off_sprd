# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import os, sys
import MyString
import Time
import re
import _thread
import Utilty
from collections import OrderedDict
import WakeLockObject
from collections import deque
import operator
#对文件操作的工具模块


# 1.将A文件复制到B文件中去(保持原来格式)
def copy_file (inputFile, outputFile, encoding):
    try:
        fin = open(inputFile, 'r',encoding = encoding) #以读的方式打开文件
        fout = open(outputFile, 'a',encoding = encoding) #以写得方式打开文件
        for eachLiine in fin.readlines(): #读取文件的每一行
            line = eachLiine.strip() #去除每行的首位空格
            fout.write(line + '\n')
    finally:
        if fin:
            fin.close()
        if fout:
            fout.close()

# 2. 读取文件中的内容,返回List列表 (加载本地词典库)
def read_file_list(inputFile, encoding):
    results = []
    try:
        fin = open(inputFile, 'r', encoding=encoding)
        for eachLiine in fin.readlines():
            line = eachLiine.strip().replace('\ufeff', '')
            results.append(line)
    finally:
        if fin:
            fin.close()
    return results

# 3.读取文件，返回文件内容
def read_file(path):
    with open(path, 'r+', encoding='UTF-8') as f:
        str = f.read()
    return str.strip().replace('\ufeff', '')

def func():
    pass


def getResult(line,address,key,result,startTime,endTime,fd_heart):
    currentTime = "2018-"+str(line)[2:16]
    if(Time.inTheTime(startTime,endTime,str(currentTime))):
        if address in result.keys():
            result[address] = int(result[address]) + 1
        else:
            result[address] = 1
        if(key == "atInfo is"):
            fd_heart.writelines(str(line,encoding='utf-8'))
        fd_heart.flush()
        fd_heart.close()  
    return result

# 4.带缓存的文件读取

# File: readline-example-3.py
def readRadioFiles(filenamelits,startTime,endTime,keyword,year,resultDirectory):
    
    isTime = False
    lineIsTime = False
    indexd = 0;
    indexc = 0;
    activeStartTime = "";
    
    
    fd_modem_active = open(resultDirectory+"\modem_active.txt",'a',encoding='utf-8')
    fd_getDataConnec = open(resultDirectory+"\getDataConnec.txt",'a',encoding='utf-8')
    fd_voice_state = open(resultDirectory+"\VOICE_STATE.txt",'a',encoding='utf-8')
    fd_data_state = open(resultDirectory+"\DATA_STATE.txt",'a',encoding='utf-8')
    result_Radio = {}
    dataConnecte = {}
    dataRadioTechnology = []
    modelActiveData = []

    for fileName in filenamelits:
        file = open(fileName,"rb")

        fd_modem_active.write(fileName + '\n')
        fd_getDataConnec.write(fileName + '\n')
        fd_voice_state.write(fileName + '\n')
        fd_data_state.write(fileName + '\n')

        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                for key,address in keyword.items():
                    
                    if str.encode(key) in line:
                    #if re.search(str.encode(key),line)!= None:
                         #内判断满足条件的行的时间是否在开始时间和结束时间内
                         #获取每行开头的时间 "2018-01-06 05:54:40类型"
                         currentTime = year+"-"+str(line)[2:16]
                         
                         if(Time.inTheTime(startTime,endTime,str(currentTime))):
                             if(key == r'LIST_CHANGED [D'):
                                 #print(str(line)[str(line).find(r"active=") + len(r"active="):str(line).find(r"active=")+len(r"active=") + 1])
                                 indexValuts =  str(line).find(r"active=") + len(r"active=")
                                 
                                 fd_modem_active.writelines(str(line,encoding='utf-8'))
                                 #只统计第一个不等于2的
                                 if int(str(line)[indexValuts:indexValuts + 1]) == 2 and activeStartTime == "":
                                     activeStartTime = currentTime
                                     #print("2="+currentTime)
                                     #print(str(line)[str(line).find(r"active=") + len(r"active="):str(line).find(r"active=")+len(r"active=") + 1])
                                 #print (str(line,encoding='utf-8'))
                                 elif int(str(line)[indexValuts:indexValuts + 1]) == 1 or int(str(line)[indexValuts:indexValuts + 1]) == 0:
                                     #print("1="+currentTime)
                                     #只计算第一个等于 1 的
                                     if(activeStartTime != 0):
                                         duractionTime = Time.DuractionTime(year,activeStartTime,currentTime)
                                         modelActiveData.append(duractionTime)
                                         #把modem active激活和释放的时间和时长输出到文本
                                         string = "StartTime="+str(activeStartTime)+">>"+"entTime"+str(currentTime)+"==="+"DuractionTime="+str(duractionTime)+"\n"
                                         fd_modem_active.writelines(string)
                                         activeStartTime = ""
                             elif key == r'DEACTIVATE_DATA_CALL 0' or key == r'DEACTIVATE_DATA_CALL 1':
                                 duractionTime = Time.DuractionTime(year,activeStartTime,currentTime)
                                 modelActiveData.append(duractionTime)
                                 #把modem active激活和释放的时间和时长输出到文本
                                 string = "StartTime="+str(activeStartTime)+">>"+"entTime"+str(currentTime)+"==="+"DuractionTime="+str(duractionTime)+"\n"
                                 fd_modem_active.writelines(string)
                                 activeStartTime = ""  
                             elif(key == r'getDataConnec'):
                                 #返回时间节点和链接或者断开的状态
                                 if str.encode("DISCONNECTED") in line:
                                     if r"断网:" in dataConnecte.keys():
                                         dataConnecte[r"断网:"] = int(dataConnecte[r"断网:"]) + 1
                                     else:
                                         dataConnecte[r"断网:"] = 1
                                 elif str.encode("CONNECTED") in line:
                                     if r"链接:" in dataConnecte.keys():
                                         dataConnecte[r"链接:"] = int(dataConnecte[r"链接:"]) + 1
                                     else:
                                         dataConnecte[r"链接:"] = 1
                                 elif str.encode("CONNECTING") in line:
                                     if r"正在链接:" in dataConnecte.keys():
                                         dataConnecte[r"正在链接:"] = int(dataConnecte[r"正在链接:"]) + 1
                                     else:
                                         dataConnecte[r"正在链接:"] = 1
                                 elif str.encode("suspended") in line:
                                     if r"暂停:" in dataConnecte.keys():
                                         dataConnecte[r"暂停:"] = int(dataConnecte[r"暂停:"]) + 1
                                     else:
                                         dataConnecte[r"暂停:"] = 1
                                 fd_getDataConnec.writelines(str(line,encoding='utf-8'))
                             elif(key == r'VOICE_REGISTRATION_STATE'):
                                 fd_voice_state.writelines(str(line,encoding='utf-8'))
                             elif(key == r'DATA_REGISTRATION_STATE'):
                                 fd_data_state.writelines(str(line,encoding='utf-8'))
                             elif(key == r'dataRadioTechnology'):
                                 dataValuts =  str(line).find(r"dataRadioTechnology=") + len(r"dataRadioTechnology=")
                                 dataRadioTechnology.append(str(line)[dataValuts:-3])
                             


#        copy_file(R"E:\a\ojhgakbkyroqrhih\heart.txt",R"E:\a\ojhgakbkyroqrhih\healthd.txt",'utf-8')
        if os.path.isfile(fileName):
            file.close

    if activeStartTime != "":
        duractionTime = Time.DuractionTime(year,activeStartTime,Time.TimeTimestampTransfer(endTime))
        modelActiveData.append(duractionTime)
        #把modem active激活和释放的时间和时长输出到文本
        fd_modem_active.writelines("到log结束的时间点，没释放的active"+"\n")
        string = "StartTime="+str(activeStartTime)+">>"+"entTime"+str(Time.TimeTimestampTransfer(endTime))+"==="+"DuractionTime="+str(duractionTime)+"\n"
        fd_modem_active.writelines(string)
        activeStartTime = ""

    fd_modem_active.flush()
    fd_modem_active.close()
    fd_getDataConnec.flush()
    fd_getDataConnec.close()
    fd_voice_state.flush()
    fd_voice_state.close()
    fd_data_state.flush()
    fd_data_state.close()
    
    if modelActiveData:
        result_Radio["modelActiveData"] = modelActiveData
    if dataConnecte:
        result_Radio["dataConnecte"] = dataConnecte
    if dataRadioTechnology:
        result_Radio["dataRadioTechnology"] = dataRadioTechnology

    return result_Radio

def readMainFiles(filenamelits,startTime,endTime,keyword,year,resultDirectory):
    
    isTime = False
    lineIsTime = False
    indexd = 0
    indexc = 0
    result = {}
    otherData = {}
    mainData = {}
    wakeUpData = {} 
    fd_heart = open(resultDirectory+"\heart.txt",'a',encoding='utf-8')
    fd_healthd = open(resultDirectory+"\healthd.txt",'a',encoding='utf-8')
    #保存锁的文本
    fd_wakeup = open(resultDirectory+"\wakeup.txt",'a',encoding='utf-8')
    #保存main信息
    fd_main = open(resultDirectory+"\main.txt",'a',encoding='utf-8')

    #保存锁的列表
    wakelockDeque = []
    #保存锁的出现次数和总共持续时间
    totalityLockDeque = OrderedDict()
    removeLock = False
    differenceLock = []

    screenOnTime = 0
    screenOnAllTime = 0
    screenOnAllNum = 0
    differenceScreenOn = []

    sensorList = []
    sensorAllNum = 0
    sensorAllTime = 0

    gpsAllNum = 0
    gpsAllTime = 0
    gpsOpenTime = 0

    wifi_on_time = ""
    wifi_on_All_time = 0
    bluetooth_on_time = ""
    bluetooth_on_All_time = 0
    mobile_data_time = ""
    mobile_data_All_time = 0

    #判断是不是展讯平台
    isSprd = False
    moreTag_dict = OrderedDict()

    for fileName in filenamelits:
        if r'slog' in fileName:
            isSprd = True
        file = open(fileName,"rb")
        fd_healthd.write(fileName + '\n')
        fd_heart.write(fileName + '\n')
        fd_wakeup.write(fileName + '\n')
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                if not str.encode("=================== beginning of main_system") in line:
                    tag = str(line)[35:].split(" ")[0]
                    tag = str(str.encode(tag),encoding='utf-8')
                    if tag != ":":
                        if(not tag in moreTag_dict.keys()):
                            moreTag_dict[tag] = 1
                        else:
                            moreTag_dict[tag] = moreTag_dict[tag] + 1
                for key,address in keyword.items():
                    if  str.encode(key) in line :
                    #if re.search(str.encode(key),line)!= None:
                         #获取每行开头的时间 "2018-01-06 05:54:40类型"
                         currentTime = year+"-"+str(line)[2:16]
                         #内判断满足条件的行的时间是否在开始时间和结束时间内
                         if(Time.inTheTime(startTime,endTime,str(currentTime))):
                            #*****************************************************************************************************
                            '''
                            统计亮屏时间和次数
                            '''
                            if r"Screen on to" == key or r'", ON' == key:
                                #获取当前行的前面时间包括毫秒
                                diffTime = str(line,encoding='utf-8')[:20]
                                #判断这个锁是否已经统计过了
                                if not diffTime in differenceScreenOn:
                                    if screenOnTime != 0:
                                        fd_main.writelines(str(currentTime)+"这个时间点亮屏，后面没有灭屏，又亮屏了")
                                        screenOnTime = currentTime
                                    else:
                                        screenOnTime = currentTime
                                    screenOnAllNum = screenOnAllNum + 1
                                    differenceScreenOn.append(diffTime)
                            if r"Screen off to" == key or r'", OFF' == key:
                                #获取当前行的前面时间包括毫秒
                                diffTime = str(line,encoding='utf-8')[:20]
                                if not diffTime in differenceScreenOn:
                                    screenOnTime_Duraction = Time.DuractionTime(year,screenOnTime,currentTime)
                                    fd_main.writelines(str(screenOnTime)+" --- "+str(currentTime)+" --- "+"亮屏时间:"+str(screenOnTime_Duraction)+"秒"+"\n")
                                    screenOnTime = 0
                                    screenOnAllTime = screenOnAllTime + screenOnTime_Duraction
                                    differenceScreenOn.append(diffTime)
                            #******************************************************************************************************
                            #输出所有的电池信息到文本
                            if str.encode(r'healthd') in line or r"healthd" == key or (str.encode(r'ACTION_BATTERY_CHANGED') in line and isSprd):
                                fd_healthd.writelines(str(line,encoding='utf-8'))
                            #视频通话时长输出到文本
                            if str.encode(r'通话总时长') in line or str.encode(r'通话时长') in line:
                                fd_main.writelines(str(line,encoding='utf-8'))
                            #输出所有的心跳信息到文本
                            if r"atInfo is" == key or r"receive heartbeat" == key or r"send broadcast on heartbeat response successful" == key:
                                #currentTime = year+"-"+str(line)[2:16]
                                fd_heart.writelines(str(line,encoding='utf-8'))
                            #******************************************************************************************************
                            #统计锁 #把锁的信息都输出到文本
                            elif r"acquireWakeLockInternal:" == key and not str.encode("RILJ") in line:
                                #获取锁的flags
                                flags = int(MyString.getIndexCher(line,",",1,"flags="),16)
                                #判断是否是唤醒锁，以下4种锁是唤醒CPU的
                                if Utilty.isWakeUpCpu(flags):
                                    #获取当前行的前面时间包括毫秒
                                    diffTime = str(line,encoding='utf-8')[:20]
                                    #获取锁的名字,并去掉前后的"号,获取lock值
                                    tag,lock = Utilty.getWakeLockInfo(str(line,encoding='utf-8'))
                                    #判断这条记录是否已经统计过了，统计过了就不加到列表里面
                                    if not Utilty.isInLockDeque(differenceLock,tag,lock,diffTime) :
                                        fd_wakeup.writelines(str(line,encoding='utf-8'))
                                        #给对象负值
                                        wakeLockObject = WakeLockObject.WakeLock(tag,lock,currentTime)
                                        #把对象加到集合里面
                                        wakelockDeque.append(wakeLockObject)
                                        #这个锁已经记录了保存
                                        diffWakeLockObject = WakeLockObject.WakeLock(tag,lock,diffTime)
                                        differenceLock.append(diffWakeLockObject)
                            elif r"releaseWakeLockInternal:" == key and not str.encode("RILJ") in line:
                                indexs = []
                                #在这里计算锁释放的时间
                                for index,wakeLock in enumerate(wakelockDeque):
                                    if str.encode(wakeLock._lock_) in line and str.encode(wakeLock._name_) in line:
                                        #判断这个锁释放已经处理并移除过了，如果相同的锁就直接移除不在计算时间
                                        if removeLock == True:
                                            fd_wakeup.writelines("name="+str(wakeLock._name_)+"=="+"lock="+str(wakeLock._lock_)+"=="+"time"+str(wakeLock._time_)+"重复锁"+"\n")
                                            #记录要移除的锁
                                            indexs.append(index)
                                        else:
                                            time = Time.DuractionTime(year,wakeLock._time_,currentTime)
                                            #释放锁的时候的打印
                                            fd_wakeup.writelines(str(line,encoding='utf-8'))
                                            #输出文本
                                            fd_wakeup.writelines(str("time="+str(wakeLock._time_)+"lock="+wakeLock._lock_+"tag="+wakeLock._name_+"锁持续:"+str(time)+"秒")+"\n")
                                            #统计锁出现的次数和总共持续时间
                                            totalityLockDeque = Utilty.addWakeLockToDeque(wakeLock._name_,totalityLockDeque,time)
                                            #记录要移除的锁
                                            indexs.append(index)
                                            #标志这个锁已经处理过并且移除过了，第二次在出现相同锁的时候直接移除不计算时间
                                            removeLock = True
                                #完成一次索引后移除的标志要设为False
                                removeLock = False
                                #从wakelockDeque移除锁
                                #因为每次移除一个元素，列表的长度就减少一位，那么原来的坐标就会变化，再按照原来的坐标去移除就不对了
                                #做法是:真正移除的坐标等于要移除的坐标减去列表的偏移
                                wakelockDeque_len = len(wakelockDeque)
                                for index in indexs:
                                    index = index - (wakelockDeque_len - len(wakelockDeque))
                                    wakelockDeque.pop(index)
                            #******************************************************************************************************
                            elif r"activate sensors" == key:
                                '''
                                sensorStutas = MyString.getIndexCher(str(line,encoding='utf-8'),",",1,"enable=").strip("\n")
                                sensorsName = MyString.getIndexCher(line,",",0,"activate sensors").strip("\"")
                                '''
                                #获取sensor的名字和状态,#状态1 代表开启 0代表关闭
                                sensorStutas,sensorsName =  Utilty.getSensorInfo(line)
                                if sensorStutas == "1":
                                    #把开启的sensor，名字和时间加入队列
                                    sensorList.append([sensorsName,currentTime])
                                elif sensorStutas == "0":
                                    for index,sensor in enumerate(sensorList):
                                        if sensorsName == sensor[0]:
                                            sensorTime = Time.DuractionTime(year,sensor[1],currentTime)
                                            fd_main.writelines(sensor[1]+"---"+str(currentTime)+">>>"+"sensor:"+sensorsName+"持续:"+str(sensorTime)+"秒"+"\n")
                                            sensorList.pop(index)
                                            sensorAllNum = sensorAllNum + 1
                                            sensorAllTime = sensorAllTime + sensorTime
                                            break
                            elif r"Call open_gps name" == key:
                                gpsOpenTime = currentTime
                                gpsAllNum = gpsAllNum + 1
                            elif r"gps_cleanup: clear init" == key:
                                gpsTime = Time.DuractionTime(year,gpsOpenTime,currentTime)
                                gpsAllTime = gpsAllTime + gpsAllTime
                                gpsOpenTime = 0
                            elif r"Global.putString(name=" == key:
                                '''
                                #获取设备名，wifi/bluetooth_on/mobile_data
                                globalName = MyString.getIndexCher(str(line,encoding='utf-8'),",",0,"name=").strip("\n")
                                #获取状态值先按","切割取第二个值，然后再按" "切割取value=后面的值 #状态1 代表开启 0代表关闭
                                value = str(line,encoding='utf-8').split(",")[1]
                                value = MyString.getIndexCher(value," ",1,"value=").strip("\n")
                                '''
                                #获取设备名，wifi/bluetooth_on/mobile_data 和开关状态值
                                globalName,value = Utilty.getGlobalInfo(str(line,encoding='utf-8'))
                                time = Time.DuractionTime(year,wifi_on_time,currentTime)
                                if globalName == "wifi_on":
                                    if value == "1":
                                        wifi_on_time = currentTime
                                    elif value == "0" and wifi_on_time != "":
                                        wifi_on_All_time = wifi_on_All_time + time
                                        wifi_on_time = ""
                                elif globalName == "bluetooth_on":
                                    if value == "1":
                                        bluetooth_on_time = currentTime 
                                    elif value == "0" and bluetooth_on_time != "":
                                        bluetooth_on_All_time =bluetooth_on_All_time + time
                                        bluetooth_on_time = ""
                                elif globalName == "mobile_data":
                                    if value == "1":
                                        mobile_data_time = currentTime 
                                    elif value == "0" and mobile_data_time != "":
                                        mobile_data_All_time = mobile_data_All_time + time
                                        mobile_data_time = ""
                            #address != r"healthd:" 为了过滤掉healthd在图片上的显示
                            elif address in mainData.keys() and address != r"healthd:" and address != r"AP唤醒CPU:" and address != r"AP释放锁:" and address != r"电量:" and address != r"灭屏:":
                                mainData[address] = int(mainData[address]) + 1
                            elif address != r"healthd:" and address != r"AP唤醒CPU:" and address != r"AP释放锁:" and address != r"电量:" and address != r"灭屏:":
                                mainData[address] = 1
                         break
#        copy_file(R"E:\a\ojhgakbkyroqrhih\heart.txt",R"E:\a\ojhgakbkyroqrhih\healthd.txt",'utf-8')
        if os.path.isfile(fileName):
            file.close
    #*****************************************************************************************************************************
    '''
     #统计没有释放的锁
    '''
    if len(wakelockDeque) > 0:
        for index,wakeLock in enumerate(wakelockDeque):
            fd_wakeup.writelines(wakeLock._time_+"-----"+"tag="+wakeLock._name_+"lock="+wakeLock._lock_+"未释放或者log已完结"+"\n")
            #统计锁出现的次数和总共持续时间
            if wakeLock._name_ in totalityLockDeque.keys():
                totalityLockDeque[wakeLock._name_][0] = totalityLockDeque[wakeLock._name_][0] + 1
                totalityLockDeque[wakeLock._name_][1] = totalityLockDeque[wakeLock._name_][1] + Time.DuractionTime(year,wakeLock._time_,Time.TimeTimestampTransfer(endTime))
            else:
                totalityLockDeque[wakeLock._name_] = [1,0]

    '''
    统计锁出现的次数和总共持续的时间
    '''
    #先排序 按字典的value值排序reverse = True取反，因为默认是从小到大
    totalityLockDeque = sorted(totalityLockDeque.items(),key = operator.itemgetter(1),reverse = True)
    #print(totalityLockDeque)
    if len(totalityLockDeque) > 0:
        for key,address in enumerate(totalityLockDeque):
            fd_wakeup.writelines(str(address[0])+"---"+"次数:"+str(address[1][0])+"时间:"+str(address[1][1])+"秒"+"\n")
    wakeUpData = totalityLockDeque
    #*****************************************************************************************************************************
    '''
    统计亮屏次数和时间
    '''
    if screenOnTime!=0:
        fd_main.writelines(str(screenOnTime)+"这个时间点亮屏，后面没有灭屏，确定是否是log完结"+"\n")
    if screenOnAllNum != 0 and screenOnAllTime != 0:
        fd_main.writelines("亮屏时间:"+str(screenOnAllTime)+"秒"+"---"+"亮屏次数:"+str(screenOnAllNum)+"\n")
    otherData["亮屏"] = [screenOnAllTime,screenOnAllNum]
    #*****************************************************************************************************************************
    '''
    统计sensor次数和时间
    '''
    if (sensorAllTime != 0 and sensorAllNum != 0) or len(sensorList) > 0:
        if len(sensorList) > 0:
             for index,sensor in enumerate(sensorList):
                 sensorAllTime = sensorAllTime + Time.DuractionTime(year,sensor[1],Time.TimeTimestampTransfer(endTime))
                 fd_main.writelines("sensor:"+sensor[0]+"---"+sensor[1]+"这个时间开启一直没关确认是否log结束"+"\n")
        fd_main.writelines("sensor时间:"+str(sensorAllTime)+"秒"+"---"+"sensor次数:"+str(sensorAllNum)+"\n")
        otherData["sensor"] = [sensorAllTime,sensorAllNum]
    #*****************************************************************************************************************************
    '''
    统计gps次数和时间
    '''
    if (gpsAllTime != 0 and gpsAllNum != 0) or gpsOpenTime != 0:
        fd_main.writelines("gps持续时间:"+str(gpsAllTime)+"秒"+"---"+"gps次数:"+str(gpsAllNum)+"\n")
        if gpsOpenTime != 0:
           fd_main.writelines("gps:"+str(gpsOpenTime)+"这个时间开启一直没关确认是否log结束"+"\n")
           gpsAllTime = gpsAllTime + Time.DuractionTime(year,gpsOpenTime,Time.TimeTimestampTransfer(endTime))
        otherData["gps"] = [gpsAllTime,gpsAllNum]
        gpsOpenTime = 0
    #*****************************************************************************************************************************
    '''
    统计wifi的运行时间
    '''
    if Time.isTime(wifi_on_time) and int(Time.TimeTransferTimestamp(wifi_on_time)) > 0:
        fd_main.writelines("wifi开启时间:"+str(wifi_on_All_time+Time.DuractionTime(year,wifi_on_time,Time.TimeTimestampTransfer(endTime)))+"秒"+"\n")
        wifi_on_time = 0
    else:
        fd_main.writelines("wifi开启时间:"+str(wifi_on_All_time)+"秒"+"\n")
        wifi_on_time = 0
    #*****************************************************************************************************************************
    '''
    统计bluetooth的运行时间
    '''
    if Time.isTime(bluetooth_on_time) and int(Time.TimeTransferTimestamp(str(bluetooth_on_time))) > 0:
        fd_main.writelines("蓝牙开启时间:"+str(bluetooth_on_All_time+Time.DuractionTime(year,bluetooth_on_time,Time.TimeTimestampTransfer(endTime)))+"秒"+"\n")
        bluetooth_on_time = 0
    else:
        fd_main.writelines("蓝牙开启时间:"+str(bluetooth_on_All_time)+"秒"+"\n")
        bluetooth_on_time = 0
    #*****************************************************************************************************************************
    '''
    统计数据流量的运行时间
    '''
    '''
    if Time.isTime(mobile_data_time) and int(Time.TimeTransferTimestamp(str(mobile_data_time))) > 0:
        fd_main.writelines("数据流量开启时间:"+str(mobile_data_All_time+Time.DuractionTime(year,mobile_data_time,Time.TimeTimestampTransfer(endTime)))+"秒"+"\n")
        mobile_data_time = 0
    else:
        fd_main.writelines("数据流量开启时间:"+str(mobile_data_All_time)+"秒"+"\n")
        mobile_data_time = 0
    '''
    #这个方法待验证
    mobile_data_time = Utilty.calculation_All_Time_Current(mobile_data_time,mobile_data_All_time,endTime,fd_main,"数据流量开启时间:",year)
    #*****************************************************************************************************************************
    more_tag_dict = sorted(moreTag_dict.items(),key = operator.itemgetter(1),reverse = True)
    for address in more_tag_dict:
        fd_main.writelines(str(address)+"\n")

    fd_healthd.flush()
    fd_healthd.close()
    fd_heart.flush()
    fd_heart.close() 
    fd_wakeup.flush()
    fd_wakeup.close()
    fd_main.flush()
    fd_main.close()

    if mainData:
        result["mainData"] = mainData
    if otherData:
        result["otherData"] = otherData
    if wakeUpData:
        result["wakeUpData"] = wakeUpData
    return result


def readKernelFiles(filenamelits,startTime,endTime,keyword,year,resultDirectory):
    
    kernelData = {}
    fd_kernel = open(resultDirectory+"\kernel.txt",'a',encoding='utf-8')
    wakeUp = False
    duractionTime = OrderedDict()
    wakeLockName = ""
    wakeUpTime = ""
    wakeUpNum = 0
#    totalityWakeUpDeque = OrderedDict()
    #为了区别计算每次唤醒相同锁出现的次数
    itme = 0
    for fileName in filenamelits:
        file = open(fileName,"rb")
        fd_kernel.write(fileName + '\n')
        while 1:
            lines = file.readlines(100000)
            if not lines:
                break
            for line in lines:
                for key,address in keyword.items():
                    #判断CPU的状态并保持到文本
                    if str.encode(key) in line:
                        #获取每行开头的时间 "2018-01-06 05:54:40类型"
                        currentTime = year+"-"+str(line)[2:16]
                        #内判断满足条件的行的时间是否在开始时间和结束时间内
                        if(Time.inTheTime(startTime,endTime,str(currentTime))):
                            '''
                            if (key == "PM: suspend exit"):
                                wakeUp = True
                                duractionTime[key] = currentTime
                            elif (wakeUp and key == "active wakeup source"):
                                #为了区别计算每次唤醒相同锁出现的次数
                                itme = itme + 1
                                #获取锁的名字
                                wakeLockName = MyString.getCherByWake(line,"active wakeup source:")
                                #过滤掉换行符，由于读取的是二进制所以先转换成utf-8编码
                                wakeLockName = str(wakeLockName,encoding = 'utf-8').strip("\n")
                                #因为会有重复的锁，所以先判断是否已经存在，就加个标志
                                if wakeLockName in duractionTime.keys():
                                    duractionTime[wakeLockName+"=="+str(itme)] = currentTime
                                else:
                                    duractionTime[wakeLockName] = currentTime
                            elif (wakeUp and key == "PM: suspend entry"):
                                wakeUp = False
                                duractionTime[key] = currentTime
                                #计算唤醒时间的总时长并计算中间的持锁的时间
                                message =  getDuractionTime(year,duractionTime)
                                #返回的结果写入文本
                                fd_kernel.writelines(message)
                                #每次结束清除掉字典
                                duractionTime.clear()
                            '''
                            if (key == "PM: suspend exit"):
                                #取PM: suspend exit后面的值
                                wakeUpTime = MyString.getCherTime(str(line,encoding='utf-8'),"PM: suspend exit ")
                                #按 "."切割，取第一个数据就是时间
                                wakeUpTime = str(wakeUpTime).split(".")[0]
                                wakeUp = True
                                wakeUpNum = wakeUpNum  + 1
                                pass
                            elif (wakeUp == True and key == "PM: suspend entry"):
                                entryTime = MyString.getCherTime(str(line,encoding='utf-8'),"PM: suspend entry ")
                                #按 "."切割，取第一个数据就是时间
                                entryTime = str(entryTime).split(".")[0]
                                wakeUpDuractionTimee = Time.DuractionTime(year,wakeUpTime,entryTime)
                                fd_kernel.writelines("唤醒时长:"+str(wakeUpDuractionTimee)+"秒"+"---"+"开始时间:"+str(wakeUpTime)+">>>"+"结束时间:"+str(entryTime)+"\n")
                                wakeUp = False
                                wakeUpTime = ""
                                entryTime = ""
                            else:
                                if address in kernelData.keys() and address != r"系统休眠:":
                                   kernelData[address] = int(kernelData[address]) + 1
                                elif address != r"系统休眠:":
                                   kernelData[address] = 1 
                                break
        if os.path.isfile(fileName):
            file.close
        '''
        #解析完成后 判断duractionTime里面是否有数据，如果有数据，说明最后唤醒后就没有在休眠了，或者log没有了，这里提个醒
        if len(duractionTime) > 0:
            #计算唤醒时间的总时长并计算中间的持锁的时间
            message =  getDuractionTime(year,duractionTime)
            #返回的结果写入文本
            fd_kernel.writelines(message)
        '''
    if wakeUpTime != "":
        fd_kernel.writelines(str(wakeUpTime)+"时间点唤醒之后没有休眠确认是否log结束"+"\n")
        fd_kernel.writelines("唤醒次数:"+str(wakeUpNum)+"\n")

    '''
    for key,address in kernelData.items():
        fd_kernel.writelines(key+str(address))
    fd_kernel.flush()
    fd_kernel.close()
    '''
    
    return kernelData



def readfiless(fileName):
    with open(fileName,"rb") as f:  
        for line in f:  
            print (line)
    
def readlines(fileName):  
    f = open(fileName, "rb")  
    for line in f:  
        if "irq: 57" in line:
            print ("57中断")  
    f.close()  

#文件的读取  

def writefile(path,content):  
    fd = file(path, "w+") #读取方式打开，清除文件原来内容  
    fd.write("content"+"\n")  
    fd.close()  
  
def writelines(path,contents):
    #以追加的方式打开如果文件不存在创建文件
    fd = open(path,'a',encoding='utf-8') 
    fd.write(contents)
#    fd.writelines(contents)      #写入列表内容  
    fd.flush()
    fd.close()  

def writefile(path,name,contents):
    os.getcwd()  #查看当前路径
    os.chdir(path)  #更改至d盘相应路径下
    course = open(name,'w',encoding='utf-8')
    course.writelines(contents)
    course.close()   #保存


#索引文件夹及子目录返回所有文件路径
def all_path(dirname):
    filelistlog = dirname + "\\filelistlog.txt"  # 保存文件路径
    postfix = set(['pdf','doc','docx','epub','txt','xlsx','djvu','chm','ppt','pptx'])  # 设置要保存的文件格式
    all_path = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            all_path.append(apath)
            '''
            if True:        # 保存全部文件名。若要保留指定文件格式的文件名则注释该句
            #if apath.split('.')[-1] in postfix:   # 匹配后缀，只保存所选的文件格式。若要保存全部文件，则注释该句

                try:
                    with open(filelistlog, 'a+') as fo:
                        fo.writelines(apath)
                        fo.write('\n')
                except:
                    pass    # 所以异常全部忽略即
            '''
    
    return all_path


'''
#返回目标时间戳和文件地址的字典
targetDirectory 目标目录
fileTag 文件类型，main，kernel，radio
'''
def getTargetFileTimeList(targetDirectory,fileTag,year):
    filenames_path = {}
    for file_path in all_path(targetDirectory):
        if fileTag in file_path:
            #截取出文件名的时间字符串rindex获得指定字符串的位置
            #获取文件名
            fileName = os.path.basename(file_path)
            #判断年是不是在文件路径里面
            if year in fileName:
                getTime = fileName[fileName.rindex(year):-4]
                getTime = getTime.replace("_"," ") #去掉时间里面的下划线
                #将"2018-01-06 05-54-40"转换为"2018-01-06 05:54:40类型"
                if len(getTime) == 19:
                    getTime = MyString.replace(getTime,13,16,":")
                else:
                    getTime = MyString.replace(getTime,14,17,":")
                #把时间转换成时间戳
                getTimes = Time.TimeTransferTimestamp(getTime)
                filenames_path[getTimes]=file_path
    return filenames_path

def un_file(targetDirectory,zip,tar):
    again = False
    for filename in  all_path(targetDirectory):
        #判断后缀名是不是.zip
        if os.path.splitext(filename)[1] == r'.zip':
            Utilty.un_zip(filename)
            os.remove(filename)
        #判断后缀名是不是.gz
        if os.path.splitext(filename)[1] == r'.gz':
            Utilty.un_tar(filename)
            os.remove(filename)
        if os.path.splitext(filename)[1] == r'.xz':
            os.system("xz -d "+filename)  
    for filename in  all_path(targetDirectory):
        if os.path.splitext(filename)[1] == r'.gz' or os.path.splitext(filename)[1] == r'.zip'or os.path.splitext(filename)[1] == r'.xz':
            again = True
    if again:
        un_file(targetDirectory,zip,tar)
    

def GetReady(init):
    #1.获得目标目录
    un_file(init._TargetDirectory,r".zip",r".tar")
    #清空输出的文件
    fd_heart = open(init._ResultDirectory+"\heart.txt",'w')
    fd_healthd = open(init._ResultDirectory+"\healthd.txt",'w')
    fd_modem_active = open(init._ResultDirectory+"\modem_active.txt",'w')
    fd_getDataConnec = open(init._ResultDirectory+"\getDataConnec.txt",'w')
    fd_voice_state = open(init._ResultDirectory+"\VOICE_STATE.txt",'w')
    fd_data_state = open(init._ResultDirectory+"\DATA_STATE.txt",'w')
    fd_kernel = open(init._ResultDirectory+"\kernel.txt",'w')

    fd_wakeup = open(init._ResultDirectory+"\wakeup.txt",'w')
    fd_main = open(init._ResultDirectory+"\main.txt",'w')

    remove_File(init._ResultDirectory+"\main_kernel.svg")
    remove_File(init._ResultDirectory+"\other.svg")
    remove_File(init._ResultDirectory+"\modem_radio.svg")
    remove_File(init._ResultDirectory+"\wakeLock.svg")

    fd_healthd.truncate()
    fd_heart.truncate()
    fd_modem_active.truncate()
    fd_getDataConnec.truncate()
    fd_voice_state.truncate()
    fd_data_state.truncate()
    fd_kernel.truncate()
    fd_main.truncate()
    fd_heart.close()
    fd_healthd.close()
    fd_modem_active.close()
    fd_getDataConnec.close()
    fd_voice_state.close()
    fd_data_state.close()
    fd_kernel.close()
    fd_wakeup.close()
    fd_main.close()


def getDuractionTime(year,duractionTime):

    massing = []
    startLockTime = 0
    startLockName = ""
    ren = len(duractionTime)
    if "PM: suspend of" in duractionTime.keys() and "PM: resume of" in duractionTime.keys():
        totalityTime = Time.DuractionTime(year,duractionTime["PM: resume of"],duractionTime["PM: suspend of"])
        massing.append("唤醒持续时长:"+str(totalityTime)+"秒"+"====="+"开始时间:"+duractionTime["PM: resume of"]+">>>>"+"结束时间:"+duractionTime["PM: suspend of"]+"\n")
    else:
        massing.append("本次唤醒之后没有休眠或者log终结唤醒时间:"+duractionTime["PM: resume of"]+"\n")
    for key,address in duractionTime.items():
        if not key == "PM: resume of":
            if startLockTime != 0 and startLockName != "":
               lockTime =  Time.DuractionTime(year,startLockTime,address)
               massing.append(startLockName+"持续了:"+str(lockTime)+"秒"+"\n")
               startLockName = key
               startLockTime = address
            else:
               startLockName = key
               startLockTime = address
    return massing



def remove_File(my_file):
    if os.path.exists(my_file):
        #删除文件，可使用以下两种方法。
        os.remove(my_file)
        #os.unlink(my_file)
    else:
        print (r'no such file:%s'%my_file)

if __name__ == '__main__':
    copy_file('../data/test1.txt', '../data/text.txt','UTF-8')
    contents = read_file_list('../dict/time.dict','UTF-8')
    print(contents)

