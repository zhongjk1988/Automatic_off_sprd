
#    inputpath = r"E:\VsProjects\mpld\mpld\Log.kernel.log"
#    outputpath = r"E:\VsProjects\mpld\mpld\kernel.txt"
import time
import sys
import os
 
def usage():
    print('''Help Information:
             kmsg_translate inputfile:   input file  to parse        
                        ''')
'''
if len(sys.argv) < 2:
    usage()
    sys.exit(2)

inpath = sys.argv[1]
print ("parameter")
print (inpath)
print ("parameter")
''' 
def calc_delta(stream,key_value):
    global s_second
    global s_microsecond
    global a_time
    global outfile
    '''
    if a_time ==None:
        print("Can't convert to android time")
        exit(-1)
    '''
    for line in stream:
        if line:
            try:
                line = str(line,encoding='utf-8')
                for key,address in key_value.items():
                    if key in line:
                        get_atime(line,key)
                begin_index =  line.index(r'[')
                end_index = line[begin_index+1:].index(']')+begin_index+1
                time_string = line[begin_index + 1 :end_index]
                [d_second,d_microsecond] = time_string.split('.')
                delta_second = int(int(d_second) - int(s_second))
                delta_microsecond = int(int(d_microsecond)-int(s_microsecond))
                [t_second, t_microsecond] = a_time.split('.')
                seconds = (delta_second + int(t_second))
                microseconds = (delta_microsecond + int(t_microsecond) * 1000)
                if microseconds < 0:
                    microseconds = microseconds + 1000000
                    seconds = seconds - 1
                times = str(seconds)
                x = time.localtime(float(times))
                realtime = time.strftime('%Y-%m-%d %H:%M:%S', x)
                new_line = realtime+ "." + str(microseconds) +' ' + line
                outputfile.writelines(new_line)
            except:
                outputfile.writelines(str(line))
 
 
def get_atime(line,key):
    global s_second
    global s_microsecond
    global a_time
    if line:
        a_time_op = line.find(key)
        if a_time_op>=1:
            begin_index =  line.index('[')
            end_index = line[begin_index+1:].index(']')+begin_index+1
            date_string = line[a_time_op + 6 :a_time_op+20]
            date_string = date_string.split(':')[0]
            #print("date_string=="+str(date_string))
            abs_time = line[begin_index + 1 :end_index]
            [s_second,s_microsecond] = abs_time.split('.')
            a_time = date_string;
            #print(date_string)
 
def timeConversion(targetFile_name,resultFile_name,key_value):
    global inputfile
    global outputfile
    '''
    if inpath == None:
        usage()
        sys.exit(2)
    '''
    
    if not os.path.exists(resultFile_name):
        open(resultFile_name,"w") 
    
    inputfile = open(targetFile_name, 'rb')
    outputfile = open(resultFile_name,'a',encoding='utf-8')
    
    #get_atime(inputfile)
    inputfile.seek(0)
    calc_delta(inputfile,key_value)
    inputfile.close()
    outputfile.close()
    #删除掉原文件
    os.remove(targetFile_name)
    #创建新的文件名
    new_resultFileName = os.path.splitext(resultFile_name)[0]+".log"
    #修改结果文件名
    os.rename(resultFile_name,new_resultFileName)

if __name__ == "__timeConversion__":
    main()
