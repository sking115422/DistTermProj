
import socket


try:
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    
    print ()
    print("Hostname :  ",host_name)
    print("IP : ",host_ip)
except:
    print ()
    print("Unable to get Hostname and IP")



HOST = host_ip  # Host broadcast IP
PORT = 44444        # Port to listen on (non-privileged ports are > 1023)

while True:
    
    print ("###################################################")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        
        print ()
        print('Connected: ', addr)
        
        with conn:
            
            machine_ip = None
            file_to_send = None
            
            while True:
                
                try:
                
                    data = conn.recv(1024)
                    
                    if data == None:
                        print ()
                        print ("No request recieved")
                        break
                    
                    try:
                        data_str = data.decode('utf-8')
                        data_list = data_str.split(" ")
                        
                    except:
                        print ()
                        print ("bytes are not covertible to ascii")
                    
                    if data_list[0] == "request":
                        
                        machine_ip = data_list[1]
                        file_to_send = data_list[2]
                
                    fo = open('./DistShared/' + file_to_send, 'rb')
                    
                    buf = fo.read(1024)

                    while len(buf) != 0:
                        
                        conn.send(buf)
                        buf = fo.read(1024)
                        print ()
                        print ("Sending: " + file_to_send)
                        
                    fo.close()
                    print ("File sent!")
                
                except:
                    print ()
                    print ("Connection closed")
                    break
                    
                        
                        
                
            
                


