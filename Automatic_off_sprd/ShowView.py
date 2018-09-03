# -*- coding: UTF-8 -*-
import numpy as np  
import matplotlib.pyplot as plt 
import matplotlib
import Utilty
plt.style.use('ggplot')
#import pandas as pd


'''
显示柱状图，用来显示main log里面的信息
'''
def showMianInfo(data):
    #加一个初始化值，让绘图Y轴从0开始
    y = []
    x = []
    y2 = []
    x2 = []
    dataY = []
    dataX = []

    index = 0
    modemActiveData = [0]
    
    if "mainData" in data.keys():
        for key,address in data["mainData"].items():
            y.append(address)
            x.append(key)
            index = index + 1

        if not y == None and not x == None:
            plt.figure(figsize=(16,9)) 
            plt.subplot(221) 
            #plt.tight_layout(pad=0.4, w_pad=2.0, h_pad=2.0)
            zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
            #index=np.arange(5)

            index=np.arange(len(x))
            plt.xticks(np.arange(len(x)),x ,fontproperties=zhfont1)
            plt.title('main&kernel 信息统计',fontproperties=zhfont1)
            datasMainData = plt.bar(left=index,height=y,color=('b','r','g','c','m'),width=0.2)
            autolabel(datasMainData)
     
    if "modelActiveData" in data.keys():
        for value in data["modelActiveData"]:
            modemActiveData.append(value)
        if modemActiveData:
            #统计列表里面的N秒出现了多少次
            modemActiveData =Utilty.getRRCTIme(modemActiveData)
            #给X,Y轴赋值
            for key,address in modemActiveData.items():
                print(address)
                y2.append(address)
                x2.append(key)
            plt.subplot(222) 
            #plt.tight_layout(pad=0.4, w_pad=2.0, h_pad=2.0)
            #只能同时改变x y轴显示的字体大小
            zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
            index = np.arange(len(x2))
            plt.xticks(np.arange(len(x2)),x2 ,fontproperties=zhfont1)
            plt.title('modem active 激活时间',fontproperties=zhfont1)
            datasmodelBar = plt.bar(left=index,height=y2,color=('b','r','g','c','m'),width=0.2)
            autolabel(datasmodelBar)


    if "dataConnecte" in data.keys():
        for key,address in data["dataConnecte"].items():
            print(str(address))
            dataY.append(address)
            dataX.append(key)
        if not dataY == None and not dataX == None:
            plt.subplot(223) 
            #plt.tight_layout(pad=0.4, w_pad=2.0, h_pad=2.0)
            #只能同时改变x y轴显示的字体大小
            zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
            index = np.arange(len(dataX))
            plt.title('网络连接状态',fontproperties=zhfont1)
            plt.xticks(np.arange(len(dataX)),dataX ,fontproperties=zhfont1)
            dataRects = plt.bar(left=index,height=dataY,color=('b','r','g','c','m'),width=0.2)
            autolabel(dataRects)
    if "dataRadioTechnology" in data.keys():
        #统计出各种类型出现的次数
        dataRadioTechnology = Utilty.getDataRadioTechnology(data["dataRadioTechnology"])
        #以出现的类型为X轴，出现的次数为Y轴
        if dataRadioTechnology:
            dataRadioY = []
            dataRadioX = []
            for key,address in dataRadioTechnology.items():
                print(str(address))
                dataRadioY.append(address)
                #转变网络制式的显示
                dataRadioX.append(Utilty.getNetworkMode(int(key)))
            if not dataRadioY == None and not dataRadioX == None:
                plt.subplot(224) 
                #plt.tight_layout(pad=0.4, w_pad=2.0, h_pad=2.0)
                #只能同时改变x y轴显示的字体大小
                zhfont1 = matplotlib.font_manager.FontProperties(fname='C:\Windows\Fonts\simkai.ttf')
                index = np.arange(len(dataRadioX))
                plt.title('数据网络注册状态',fontproperties=zhfont1)
                plt.xticks(index,dataRadioX ,fontproperties=zhfont1)
                rects = plt.bar(left=index,height=dataRadioY,color=('b','r','g','c','m'),width=0.2)
                autolabel(rects)
    plt.tight_layout()
    plt.show()
        #plt.savefig(r'E:\plot1.png', format='png')  


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % float(height))


def showRadioInfo(datax,datax2):
    x2 = []
    y2 = []
    y = []
    x = []

    for data in datax:

        x2.append(data)
        y2.append(5)
    for data in datax2:
        x.append(data)
        y.append(5)
    #z = np.cos(x**2)  
    
    
    if not x == None and not y == None:
        plt.plot(x,y,label="sin(x)",color="red")  
    if not x2 == None and not y2 == None:
        plt.plot(x2,y2,"*",label="cos(x^2)")  
    plt.xlabel("Time(s)")  
    plt.ylabel("Volt")  
    plt.title("PyPlot First Example")  
    #y轴的限制
    plt.ylim(0,10)  
    plt.legend()  
    plt.show()  

'''
#随机生成两个dataframe
d1 = pd.DataFrame(columns=['x', 'y'])
d1['x'] = np.random.normal(0, 1, 100)
d1['y'] = np.random.normal(0, 1, 100)
d2 = pd.DataFrame(columns=['x', 'y'])
d2['x'] = np.random.normal(2, 1, 100)
d2['y'] = np.random.normal(2, 1, 100)

#分别画出scatter图，但是设置不同的颜色
plt.scatter(d1['x'], d1['y'], color='blue', label='d1 points')
plt.scatter(d2['x'], d2['y'], color='green', label='d2 points')

#设置图例
plt.legend(loc=(1, 0))

#显示图片
plt.show()
'''

'''
x = (5,5,5,5,5,5,5,5,5,20)
y = (5,5,5,5,5,5,5,5,5,5)

x2 = (5,5,5,5,5,5,5,5,5,20)
y2 = (5,5,5,5,5,5,5,5,5,5)
#z = np.cos(x**2)  
  
plt.figure(figsize=(8,4))  
plt.plot(x,y,label="sin(x)",color="red",linewidth=2)  
plt.plot(x2,y2,"b--",label="cos(x^2)")  
plt.xlabel("Time(s)")  
plt.ylabel("Volt")  
plt.title("PyPlot First Example")  
#y轴的限制
plt.ylim(0,10)  
plt.legend()  
plt.show()  
'''

'''
def plot_curve1(data,title):
    fig1 = plt.figure(figsize=(15,5))
    ax1 = fig1.add_subplot(1,1,1)
    ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))#设置时间标签显示格式
    plt.xticks(pd.date_range('2014-09-01','2014-09-30'),rotation=90)
    plt.title(title)
    plt.plot(data,'o-')
    plt.show()
'''
