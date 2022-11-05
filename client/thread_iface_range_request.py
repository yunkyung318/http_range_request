import os
import sys
import subprocess
import threading
import math

ip1_data = " "
ip2_data = " "

ip1_throughput = 0
ip2_throughput = 0

system = 0
buf = None

start = 0
end = 500000
chunk1 = 500000 #default chunk suze
chunk2 = 500000

file_size = 0

server = "http://192.168.2.45:8000"
ip1 = "192.168.2.46"  #wlan0, 2G
ip2 = "192.168.2.43"  #wlan1, 5G

#lock = threading.Lock()

os.system('touch video.mp4')

def command(ip) :
    command = "sudo curl --interface "+ip+" "+server
    return os.popen(command).read()

def range_command(ip, chunk) :
    global start, end, system
    
    if ip == ip1 :
        filename = "buf1.mp4"
        print("wlan0 start", start)
        print("wlan0 end", end)
        print("wlan0 chunk", chunk)
    elif ip == ip2 :
        filename = "buf2.mp4"
        print("wlan1 start", start)
        print("wlan1 end", end)
        print("wlan1 chunk", chunk)

    command = "sudo curl -w \"@format.txt\" --interface "+ip+" "+server+"/video -H \"Range: "+str(start)+"-"+str(end)+"\" -o "+filename
    
    start = end + 1
    end += chunk + 1
    
    if end == int(file_size) :
        pass
    elif end == int(file_size) or end >= int(file_size) :
        end = int(file_size)
        system = 1

    throughput = os.popen(command).read()

    cat_file = "cat " + filename
    result = subprocess.check_output(cat_file, shell=True)
    return result, throughput, chunk

def download(ip, chunk) :
    global ip1_throughput, ip1_data, chunk1
    global ip2_throughput, ip2_data, chunk2
    print("----------------------------------------------------------------")
    
    data, throughput, chunk = range_command(ip, chunk)

    if ip == ip1 :
        ip1_throughput = throughput
        ip1_data = data
        chunk1 = chunk
        print("ip1_throughput", ip1_throughput)
        print("chunk1", chunk1)
    elif ip == ip2 :
        ip2_throughput = throughput
        ip2_data = data
        chunk2 = chunk
        print("ip2_throughput", ip2_throughput)
        print("chunk2", chunk2)

    print("----------------------------------------------------------------")
    
file_size = command(ip1)

wlan0 = threading.Thread(target=download, args=(ip1, chunk1))
wlan1 = threading.Thread(target=download, args=(ip2, chunk2))

wlan0.start()
wlan1.start()

while system != 1 :
    wlan0.join()
    wlan1.join()
    
    buf = None
    buf = ip1_data + ip2_data
    
    with open("video.mp4", "ab") as f:
     f.write(buf)
    
    chunk1 = 500000 #default chunk suze
    chunk2 = 500000

    if int(ip1_throughput) > int(ip2_throughput) :
        result = int(ip1_throughput) / int(ip2_throughput)
        result = math.ceil(result)
        print("ip1의 throughput이 더 좋음",result)
        chunk1= chunk1 * result
        print("chunk1 ",chunk1)
    else :
        result = int(ip2_throughput) / int(ip1_throughput)
        print(result)
        result = math.ceil(result)
        print("ip2의 throughput이 더 좋음",result)
        chunk2 = chunk2 * result
        print("chunk2 ",chunk2)
    
if __name__ == "__main__" :
    thread = []

    
#if system == 1 :
#    os.exit()
"""
with open("video.mp4", "ab") as f:
    f.write(buf)
    
chunk1 = 500000 #default chunk suze
chunk2 = 500000

if int(ip1_throughput) > int(ip2_throughput) :
    result = int(ip1_throughput) / int(ip2_throughput)
    result = math.ceil(result)
    print("ip1의 throughput이 더 좋음",result)
    chunk1= chunk1 * result
    print("chunk1 ",chunk1)
else :
    result = int(ip2_throughput) / int(ip1_throughput)
    print(result)
    result = math.ceil(result)
    print("ip2의 throughput이 더 좋음",result)
    chunk2 = chunk2 * result
    print("chunk2 ",chunk2)
"""
