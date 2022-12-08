import os
import sys
import subprocess
import math
import time
import threading

ip1_data = " "
ip2_data = " "

start = 0
end = 1000000
chunk = 1000000

system = 0
file_size = 0
buf = None

server = "http://192.168.2.16:8000"
ip1 = "192.168.2.44"  #wlan0, 2G

start_time = time.time()
os.system('rm video.mp4')
os.system('touch video.mp4')

def command(ip) :
    command = "sudo curl --interface "+ip+" "+server
    return os.popen(command).read()

def range_command(ip) :
    global start, end, system
   
    if end > int(file_size) :
        end = int(file_size)
        system = 1  
    
    if start != 0 :
        start += 1
        end += chunk + 1

    command = "sudo curl "+server+"/video -H \"Range: "+str(start)+"-"+str(end)+"\" -o buf.mp4"
   
    os.system(command)
    result = subprocess.check_output("cat buf.mp4", shell=True)
    
    start = end

    return result

file_size = command(ip1)

while 1 :

    file_byte = os.path.getsize('./video.mp4')
    print('[ FILE SIZE : ', file_byte, ']')

    print("----------------------------------------------------------------")
    
    ip1_data = range_command(ip1)
    
    with open("video.mp4", "ab") as f :
            f.write(ip1_data)
    
    if system == 1 :
        with open("video.mp4", "ab") as f :
            f.write(ip1_data)

        second = time.time() - start_time
        minute = second // 60
        second = second - (minute * 60)

        time_buf = "총 다운로드 시간 "+str(minute)+"분 "+str(second)+"초"
        os.system("echo %s >> no_algo.txt"%time_buf)
        
        os.exit()
