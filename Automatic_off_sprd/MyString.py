#!/usr/bin/env python
# encoding: utf-8

'''
替换指定位置的字符，并返回
str 要替换的字符串
shiftnum，shiftnum2要替换的字符串的位置
Character 要替换的字符串
'''
def replace(str,shiftnum,shiftnum2,Character):
     getTimes = list(str)
     getTimes[shiftnum] = Character
     getTimes[shiftnum2] = Character
     return ''.join(getTimes)


if __name__ == '__main__':
    print("String_self")

'''
根据时间戳和文件的字典和开始时间结束时间获得目标文件列表
targetTime 时间戳和文件的字典
startTime  开始时间
endTime    结束时间
返回大于开始时间小于结束时间的文件，和返回小于且最接近开始时间的文件
'''
def getTargetfilename(targetTime,startTime,endTime):
    filenames = []
    timediff = 0
    for name,address in targetTime.items():
        #把大于开始时间小于结束时间的文本路径添加到列表中
        if(name >= startTime and name <= endTime):
            filenames.append(address)
        #小于且最接近开始时间的文件的时间戳
        if(name < startTime):
            if(name > timediff):
                #print("name===",name)
                timediff = name
    #把小于且最接近开始时间的文件添加到列表中
    if(timediff > 0):
        #print("namesss===",name)
        filenames.append(targetTime[timediff])
    return filenames

'''
返回关键字后面的字符
line传入的字符串
values关键字
'''
def getCher(line,values):
    result = None
    if(not line == None and not values == None):
        index = str(line).find(values) + len(values)
        result = str(line)[index:]
    return result

'''
返回关键字后面的字符
line传入的字符串
values关键字
'''
def getCherByWake(line,values):
    result = None
    if(not line == None and not values == None):
        index = str(line).find(values) + len(values)
        result = line[index-1:]
    return result

'''
返回字符串按字符切割后的列表的第n个数据
line传入的字符串
cher字符切割的关键字
index列表的位置
返回values后面的字符
'''
def getIndexCher(line,cher,index,values):
    line = str(line).split(cher)
    return getCher(line[index],values)
    
'''
返回关键字后面的字符
line传入的字符串
values关键字
'''
def getCherTime(line,values):
    result = None
    if(not line == None and not values == None):
        index = str(line).find(values) + len(values)
        result = line[index:]
    return result