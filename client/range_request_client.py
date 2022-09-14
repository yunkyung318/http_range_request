import os
import sys

if len(sys.argv) != 4:
    print("sudo python range_request_client [ip] [file_type] [Range]")
    sys.exit()
else :
    ip = sys.argv[1]
    file_type = sys.argv[2]
    file_range = sys.argv[3]

command = " "
buf = " "
data1 = " "
data2 = " "
data3 = " "

if file_type == "text" :
    command = "curl "+ip+":8000/"+file_type+" -H \"Range: "+file_range+"\""
    
    file_range = file_range.split('-')
    start = int(file_range[0])
    end = int(file_range[1])

    read_data = os.popen(command).read()
    read_data = read_data.split()
    
    file_len = int(read_data[0])
    data1 = read_data[1]
    
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
else :
    print("type is text")
    exit()
'''
elif file_type == "image" :
    command = "curl -o "+file_type+".png http://192.168.2.16:8000/"+file_type+" -H \"Range: "+file_range+"\""
    print(command) 

    file_range = file_range.split('-')
    start = int(file_range[0])
    end = int(file_range[1])

    read_data = os.popen(command).read()
    print(read_data)
    read_data = read_data.split()
    print(read_data) 
    file_len = int(read_data[0])
    data1 = read_data[1]
    
    if start == 0 :
        start = end+1
        end = file_len-1
        
        command = "curl http://192.168.2.16:8000/"+file_type+" -H \"Range: "+str(start)+"-"+str(end)+"\""
        
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
        
        command = "curl http://192.168.2.16:8000/"+file_type+" -H \"Range: "+str(start1)+"-"+str(end1)+"\""
        read_data_2 = os.popen(command).read()
        read_data_2 = read_data_2.split()

        data2 = read_data_2[1]

        # 3 curl
        
        start2 = end+1
        end2 = file_len-1
    
        command = "curl http://192.168.2.16:8000/"+file_type+" -H \"Range: "+str(start2)+"-"+str(end2)+"\""
        read_data_3 = os.popen(command).read()
        read_data_3 = read_data_3.split()

        data3 = read_data_3[1]
        
        buf = data2 + data1 + data3
         
        os.system('touch %s.png'%file_type)
        os.system('echo %s >> %s.png'%buf%file_type)
'''
