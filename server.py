
import socket


try:
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print("Hostname :  ",host_name)
    print("IP : ",host_ip)
except:
    print("Unable to get Hostname and IP")



HOST = host_ip  # Host broadcast IP
PORT = 44444        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        
        print('Connected: ', addr)
        
        machine_ip = None
        file_to_send = None
        
        while data != None:
            data = conn.recv(1024)
            print(data)
            
            try:
                data_str = str(data)
                data_list = data_str.split(" ")
                
            except:
                print("bytes are not covertible to ascii")
                
            
            if data_list[0] == "request":
                
                machine_ip = data_list[1]
                file_to_send = data_list[2]
                
            else:
            
                if file_to_send != None:
                    
                    fo = open('./DistShared/' + file_to_send, 'rb')
                    buf = fo.read(1024)
                    print("Sending: " + file_to_send + " ...")
                    
                    while buf:
                        
                        fo.send(buf)
                        buf = fo.read(1024)
                        print("Sending: " + file_to_send + " ...")
                        
                    fo.close()
                    print ("File sent!")
                    
                        
                        
                
            
                


