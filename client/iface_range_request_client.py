import os
import sys

command = " "

data1 = " "
data2 = " "

start = 0
chunk = 1000 #default chunk suze

ip1 = "169.254.173.173"
ip2 = "169.254.219.127"

def throughput(chunk, rtt) :
    throughput = chunk / rtt
    return throughput

command = "sudo curl -w \"@format.txt\" --interface "+ip1+" http://169.254.22.166:8000"
ip1_rtt = os.popen(command).read()
ip1_rtt = ip1_rtt.split()
print(ip1_rtt)
file_size = ip1_rtt[0]
chunk = sys.getsizeof(file_size)

ip1_rtt = float(ip1_rtt[2])
ip1_throughput = throughput(chunk,ip1_rtt)

print(chunk)
print(file_size)
print(ip1_rtt)
print(ip1_throughput)
"""
command = "sudo curl -w \"format.txt\" --interface "+ip2+" http://169.254.22.166:8000"
ip1_rtt = os.popen(command).read()
ip1_rtt = ip1_rtt.split()
file_size = ip1_rtt[0]
ip1_rtt = ip1_rtt[2]

print(file_size)
print(ip1_rtt)
command = "sudo curl --interface "+ip1+" http://169.254.22.166:8000/text -H \"Range: "+str(start)+"-"+str(50000)+"\""
read_data = os.popen(command).read()
read_data = read_data.split()

file_len = int(read_data[0])
data1 = read_data[1]

start = 50000 + 1
end = file_len

print("dd")
command = "sudo curl --interface "+ip2+" http://169.254.22.166:8000/text -H \"Range: "+str(start)+"-"+str(50000)+"\""

read_data2 = os.popen(command).read()
read_data2 = read_data2.split()

file_len2 = int(read_data2[0])
data2 = read_data2[1]

buf = data1 + data2

os.system('touch download.txt')
os.system('echo %s >> download.txt'%buf)
"""
"""
if start == 0 :
        start = end+1
        end = file_len-1

        command = "curl "+ip+":8000/"+file_type+" -H \"Range: "+str(start)+"-"+str(end)+"\""

        read_data_2 = os.popen(command).read()
        read_data_2 = read_data_2.split()

        data2 = read_data_2[1]

        buf = data1 + data2

        os.system('touch %s.txt'%file_type)
        os.system('echo %s >> text.txt'%buf)

    elif start > 0 :
        # 1 curl
        start1 = 0
        end1 = start-1

        command = "curl "+ip+":8000/"+file_type+" -H \"Range: "+str(start1)+"-"+str(end1)+"\""
        read_data_2 = os.popen(command).read()
        read_data_2 = read_data_2.split()

        data2 = read_data_2[1]

        # 3 curl

        start2 = end+1
        end2 = file_len-1

        command = "curl "+ip+":8000/"+file_type+" -H \"Range: "+str(start2)+"-"+str(end2)+"\""
        read_data_3 = os.popen(command).read()
        read_data_3 = read_data_3.split()

        data3 = read_data_3[1]

        buf = data2 + data1 + data3

        os.system('touch %s.txt'%file_type)
        os.system('echo %s >> %s.txt'%(buf,file_type))
    else :
        exit()
    """
