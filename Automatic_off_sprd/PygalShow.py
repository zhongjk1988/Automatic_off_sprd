import random
import pygal
from collections import OrderedDict
import Utilty
import os
class PygalShow(object):

    def __init__(self, data,targetDirectory):
        self.data = data
        self.targetDirectory = targetDirectory

    def getMainData_svg(self):
        main_dataDict = OrderedDict()
        if "mainData" in self.data.keys():
            for key,address in self.data["mainData"].items():
                main_dataDict[key] = address

        x_labels = []
        main_plot_dicts = []
        if main_dataDict:
            for key,value in main_dataDict.items():
                main_plot_dict = {
                     'value' : value,
                     'label' : str("次数:"),
                    }
                main_plot_dicts.append(main_plot_dict)
                x_labels.append(key)
            self.savePygal_svg(self.targetDirectory+'\main_kernel.svg',"自动分析main&kernel",x_labels,main_plot_dicts)
    #########################################################################################################
    def getOtherData_svg(self):
        other_dataDict = OrderedDict()
        x_labels = []
        other_plot_dicts = []
        if "otherData" in self.data.keys():
            for key,address in self.data["otherData"].items():
                other_dataDict[key] = address

        if other_dataDict and "otherData" in self.data.keys():
            for key,value in other_dataDict.items():
                other_plot_dict = {
                     'value' : value[1],
                     'label' : str("总时长:"+str(round(value[0]/60,3))+"分钟"),
                    }
                other_plot_dicts.append(other_plot_dict)
                x_labels.append(key)
            self.savePygal_svg(self.targetDirectory+'\other.svg','各项运行时间',x_labels,other_plot_dicts)
    #########################################################################################################
    def getWakeLockData_svg(self):
        wakeLock_dataDict = OrderedDict()
        x_labels = []
        wakeLock_plot_dicts = []
        if "wakeUpData" in self.data.keys():
            for key,address in enumerate(self.data["wakeUpData"]):
                #时长大于一分钟，或者次数大于10次
                if address[1][1] > 60 or address[1][0] > 10:
                    wakeLock_dataDict[address[0]] = address[1]
        if wakeLock_dataDict and "wakeUpData" in self.data.keys():
            for key,value in wakeLock_dataDict.items():
                wakeLock_plot_dict = {
                     'value' : value[0],
                     #把秒转换成分钟取小数点后三位
                     'label' : str("总时长:"+str(round(value[1]/60,3))+"分钟"),
                    }
                wakeLock_plot_dicts.append(wakeLock_plot_dict)
                x_labels.append(key)
            self.savePygal_svg(self.targetDirectory+'\wakeLock.svg','唤醒锁',x_labels,wakeLock_plot_dicts)
    #########################################################################################################
    def getRadioData_svg(self):
        radioDataDict = OrderedDict()
        modemActiveData = [0]
        model_plot_dicts = []
        dataConnecte_plot_dicts = []
        dataRadio_plot_dicts = []
        x_labels = []
        '''
        获取收集上来的数据并赋值给radioDataDict字典
        '''
        if "modelActiveData" in self.data.keys():
            for value in self.data["modelActiveData"]:
                modemActiveData.append(value)
            if modemActiveData:
                #统计列表里面的N秒出现了多少次
                modemActiveData =Utilty.getRRCTIme(modemActiveData)
                for key,address in modemActiveData.items():
                    radioDataDict[key] = address
        if "dataConnecte" in self.data.keys():
            for key,address in self.data["dataConnecte"].items():
                radioDataDict[key] = address
        if "dataRadioTechnology" in self.data.keys():
            #统计出各种类型出现的次数
            dataRadioTechnology = Utilty.getDataRadioTechnology(self.data["dataRadioTechnology"])
            #以出现的类型为X轴，出现的次数为Y轴
            for key,address in dataRadioTechnology.items():
                #转变网络制式的显示Utilty.getNetworkMode(int(key))
                radioDataDict[Utilty.getNetworkMode(int(key))] = address
        #############################################################################################################

        '''
        给x_labels赋值，并且给每个y_labels赋值，如果对应的x_labels上面没有y_labels的设置为None
        '''
        for key,value in radioDataDict.items():
            if "modelActiveData" in self.data.keys():
                if modemActiveData:

                    model_plot_dict = self.getDict(key,value,modemActiveData)
                    model_plot_dicts.append(model_plot_dict)
            if "dataConnecte" in self.data.keys():
                if key in self.data["dataConnecte"].keys():
                    dataConnecte_plot_dict = {
                         'value' : value,
                         'label' : str("次数:"),
                        }
                else:
                    dataConnecte_plot_dict = None
                dataConnecte_plot_dicts.append(dataConnecte_plot_dict)
            if "dataRadioTechnology" in self.data.keys():
                if str(Utilty.getNetworkValue(key)) in dataRadioTechnology.keys():
                    dataRadio_plot_dict = {
                         'value' : value,
                         'label' : str("次数:"),
                        }
                else:
                    dataRadio_plot_dict = None
                dataRadio_plot_dicts.append(dataRadio_plot_dict)
            x_labels.append(key)

        # 条形图spacing 设置右边标题和图的距离，margin=100 图和外边的距离,print_values显示值不用放鼠标上去，print_values_position显示值的位置
        hist = pygal.Bar(spacing = 1,margin_top = 10,margin_left = 10,height = 400,print_values=True,print_values_position='bottom')
        hist.title = 'radio分析'
        # x轴坐标
        hist.x_labels = x_labels
        # x、y轴的描述
        #hist.x_title = '状态'
        #hist.y_title = '次数'
    
        # 添加数据， 第一个参数是数据的标题
        if "modelActiveData" in self.data.keys():
            hist.add("",model_plot_dicts)
        if "dataConnecte" in self.data.keys():
            hist.add("",dataConnecte_plot_dicts)
        if "dataRadioTechnology" in self.data.keys():
            hist.add("",dataRadio_plot_dicts)
        # 保存到本地，格式必须是svg
        hist.render_to_file(self.targetDirectory+'\modem_radio.svg')

    def getDict(self,key,value,data):
        if key in data.keys():
            plot_dict = {
                 'value' : value,
                 'label' : str("次数:"),
                }
        else:
            plot_dict = None
        return plot_dict


    def savePygal_svg(self,svg_name,title,x_labels,dicts):
        try:
            # 条形图spacing 设置右边标题和图的距离，margin=100 图和外边的距离,print_values显示值不用放鼠标上去，print_values_position显示值的位置
            hist = pygal.Bar(spacing = 1,margin_top = 10,margin_left = 10,height = 300,print_values=True,print_values_position='bottom')
            hist.title = title
            # x轴坐标
            hist.x_labels = x_labels
            # x、y轴的描述
            #hist.x_title = '状态'
            #hist.y_title = '次数'
            # 添加数据， 第一个参数是数据的标题
            hist.add("",dicts)
            # 保存到本地，格式必须是svg
            hist.render_to_file(svg_name)
            #hist.add_xml_filter(self.targetDirectory+'\index.html')
            #在浏览器中显示
            #hist.render_in_browser()
        except Exception as e:
            print("svg保存错误"+e)

    def show(self):
        try:
            self.getMainData_svg()
            self.getRadioData_svg()
            self.getOtherData_svg()
            self.getWakeLockData_svg()
            os.system(self.targetDirectory+'\index.html')
        except Exception as e:
            print("show的失败:",e)
            input('press enter key to exit') 








        

