

import socket
import mysql.connector
import os


#function to connect with our MySQL database

def connect_to_db ():
    db = mysql.connector.connect(
        host='173.230.133.41',
        user='user',
        password=''
    )

    print ()
    print (db)

    mycursor = db.cursor()
    
    return db, mycursor



#Function to return the local IP and hostname

def get_local_ip():
    
    local_ip_vm = None
    
    # For broadcast IP if avaliable/necessary
    
    try:
    
        os.system("hostname -I > machine_ip.txt ")
        
        with open('machine_ip.txt') as f:
        
            tmp = str(f.readlines()[0])

        f.close()

        os.system("rm machine_ip.txt")

        tmplist = tmp.split(" ")

        for each in tmplist:
            
            if each [0:3] == '172':    
                local_ip_vm = each   
    
    except:
        
        print("hostname -I command not avaliable for this OS") 
    
        
    #For get IP associated with hostname 
    
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
    except:
        print("Unable to get Hostname and IP")
        
        
    if local_ip_vm != None:
        host = local_ip_vm
    else:
        host = host_ip
    
    print()
    print("Machine Info: (" + host_name + ")   " + host)
    print()
        
    return host, host_name

        

#Function to return all files names in DistShared folder

def get_files():
    
    files = os.listdir('DistShared')
    
    print()
    print("Files From Share Drive:")
    for item in files:
        print(item)
        
    return files



#Function to push all files from DistShared folder to server

def push_to_server ():
    
    db, mycursor = connect_to_db()
    host_ip, host_name = get_local_ip()
    files = get_files()

    print()
    for item in files:
        
        mycursor.execute("USE CDS;")
        
        sql_cmd = "INSERT INTO peer_list (IP, filename) VALUES ("
        iVals = ("'" + host_ip + "', '" + item + "'")
        
        print("Inserted file:   " + item)
        
        mycursor.execute(sql_cmd + iVals + ");")
        
        db.commit()
        

#Function to pull all files down from the server and display for user

def pull_from_server ():
    
    db, mycursor = connect_to_db ()
    
    mycursor.execute("USE CDS")
    mycursor.execute("SELECT * FROM peer_list")
    result = mycursor.fetchall()
    
    print()
    print('Avaliable Files For Download')
    print()
    
    pairlist = []
    count = 0
    for row in result:
        pair = []
        pair = [row[1], row[2]]
        pairlist.append(pair)
        count = count + 1
        
        print(str(count) + ')   Machine IP Address:   ', row[1] + '      File Name:   ' + row[2])
        
    return pairlist


#Function to delete all files from the server associate with the local IP of current machine

def delete_files ():
    
    db, mycursor = connect_to_db ()
    host_ip, host_name = get_local_ip()
    
    mycursor.execute("USE CDS")
    mycursor.execute("DELETE FROM peer_list WHERE IP = '" + host_ip + "';" )
    
    db.commit()
    
    print ()
    print ("All files associated with this machines IP have been successfully deleted from the server! ")
    
    
def main ():
    
    delete_files()
    push_to_server ()
    
    host_ip, host_name = get_local_ip()
        
    filepath = 'machine_ip.txt'

    if os.path.exists(filepath):
        
        os.system("rm " + filepath)
        
    os.system("touch " + filepath)
        
    with open(filepath, 'w') as f:
        f.write(host_ip)       
        
    HOST = host_ip # Host broadcast IP
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
                    
                    
if __name__ == "__main__":
    main()