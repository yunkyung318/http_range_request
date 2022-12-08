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
chunk1 = 1000000 #default chunk suze
chunk2 = 1000000

system = 0
file_size = 0
buf = None

server = "http://192.168.2.45:8000"
ip1 = "192.168.2.46"  #wlan0, 2G
ip2 = "192.168.2.43"  #wlan1, 5G

os.system('touch video.mp4')

def command(ip) :
    command = "sudo curl --interface "+ip+" "+server
    return os.popen(command).read()

def range_command(ip, chunk) :
    global start, end, system
   
    if end > int(file_size) :
        end = int(file_size)
        system = 2  
    
    start = end + 1
    end += chunk + 1

    command = "sudo curl -w \"@format.txt\" --interface "+ip+" "+server+"/video -H \"Range: "+str(start)+"-"+str(end)+"\" -o buf.mp4"
    
    throughput = os.popen(command).read()

    result = subprocess.check_output("cat buf.mp4", shell=True)
    return result, throughput, chunk

file_size = command(ip1)
while 1 :
    file_byte = os.path.getsize('./video.mp4')
    print('[FILE SIZE : ', file_byte, ']')
    
    buf = None

    print("----------------------------------------------------------------")
    
    ip1_data, ip1_throughput, chunk1 = range_command(ip1, chunk1)
    
    if system == 2 :
        with open("video.mp4", "ab") as f:
            buf = ip1_data
            f.write(buf)
        os.exit()

    ip2_data, ip2_throughput, chunk2 = range_command(ip2, chunk2)

    if system == 2 :
        with open("video.mp4", "ab") as f:
            buf = ip1_data + ip2_data
            f.write(buf)
        os.exit()

    buf = ip1_data + ip2_data
    
    with open("video.mp4", "ab") as f:
        f.write(buf)
     
    chunk1 = 1000000 #default chunk suze
    chunk2 = 1000000
    
    if int(ip1_throughput) > int(ip2_throughput) :
        result = int(ip1_throughput) / int(ip2_throughput)
        result = math.ceil(result)
        chunk1 = chunk1 * result
        print("wlan0 의 변경된 chunk1",chunk1)
    else :
        result = int(ip2_throughput) / int(ip1_throughput)
        result = math.ceil(result)
        chunk2 = chunk2 * result
        print("wlan1 의 변경된 chunk2 ",chunk2)

    print("----------------------------------------------------------------")

def test(ip) :
    chunk1 = 1000000 #default chunk suze
    chunk2 = 1000000
    
    if int(ip1_throughput) > int(ip2_throughput) :
        result = int(ip1_throughput) / int(ip2_throughput)
        result = math.ceil(result)
        chunk1 = chunk1 * result
        print("wlan0 의 변경된 chunk1",chunk1)
    else :
        result = int(ip2_throughput) / int(ip1_throughput)
        result = math.ceil(result)
        chunk2 = chunk2 * result
        print("wlan1 의 변경된 chunk2 ",chunk2)

    file_byte = os.path.getsize('./video.mp4')
    print('[FILE SIZE : ', file_byte, ']')
    
    buf = None

    threading.Timer(0, test(ip1)).start()
    threading.Timer(0, test(ip2)).start()

test()
