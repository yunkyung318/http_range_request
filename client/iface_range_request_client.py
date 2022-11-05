import os
import sys
import subprocess
import threading

data1 = " "
data2 = " "

system = 0

start = 0
end = 1000000
chunk1 = 1000000 #default chunk suze
chunk2 = 1000000

file_size = 0
buf = None
buf_buf = " "

ip1 = "192.168.200.17"  #wlan1
ip2 = "192.168.100.17"  #wlan0

os.system('touch video.mp4')

def command(ip) :
    command = "sudo curl --interface "+ip+" http://169.254.22.166:8000"
    return os.popen(command).read()

def range_command(ip, chunk) :
    global start, end

    print("start", start)
    print("end", end)
    print("chunk", chunk)

    command = "sudo curl -w \"@format.txt\" --interface "+ip+" http://169.254.22.166:8000/video -H \"Range: "+str(start)+"-"+str(end)+"\" -o buf.mp4"
    
    start = end + 1
    end += chunk + 1
    
    if end == int(file_size) :
        pass
    elif end == int(file_size) or end >= int(file_size) :
        end = int(file_size)
        system = 1

    throughput = os.popen(command).read()

    result = subprocess.check_output("cat buf.mp4", shell=True)
    return result, throughput, chunk

file_size = command(ip1)
i=0

while 1 :
    buf = None
    buf_buf = ""

    print("----------------------------------------------------------------")
    
    ip1_data, ip1_throughput, chunk1 = range_command(ip1, chunk1)
    print("wlan0 throughput : ", ip1_throughput)

    ip2_data, ip2_throughput, chunk2 = range_command(ip2, chunk2)
    print("wlan1 throughput : ", ip2_throughput)

    buf_buf = ip1_data + ip2_data
    
    #if buf == None : 
    buf = buf_buf
    #else : 
    #    buf += buf_buf
    
    with open("video.mp4", "ab") as f:
        f.write(buf)
    
    if system == 1 :
        os.exit()

    chunk1 = 100000 #default chunk suze
    chunk2 = 100000
    
    if int(ip1_throughput) > int(ip2_throughput) :
        result = int(ip1_throughput) // int(ip2_throughput)
        print(result)
        chunk1 = chunk1 * result
        print("chunk1 ",chunk1)
    else :
        result = int(ip2_throughput) // int(ip1_throughput)
        print(result)
        chunk2 = chunk2 * result
        print("chunk2 ",chunk2)

    print("----------------------------------------------------------------")
    #i+=1

