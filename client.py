

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
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print()
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
    except:
        print("Unable to get Hostname and IP")
        
    return host_ip, host_name


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
        pair = [row[0], row[1]]
        pairlist.append(pair)
        count = count + 1
        
        print(str(count) + ')   Machine IP Address:   ', row[0] + '      File Name:   ' + row[1])
        
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
    


#Main driver function for client

def main():
    
    delete_files()
    push_to_server ()
    pairlist = pull_from_server ()
    
    print ()
    print ("Please enter the index number of the file you wish to download!\n")
    fileindex = int(input())
    
    dest_ip = pairlist [fileindex - 1][0]
    filename = pairlist [fileindex - 1][1]
    
    print ("You are asking for file: " + filename + " from IP address: " + dest_ip + ". Correct? (Y/n)\n")
    proceed = input()
    
    if proceed == 'n' or 'N':
        print("Program terminating...")
        exit()
        
    fin = open("./Downloads/" + filename, "wb")
        
    HOST = dest_ip  # The server's hostname or IP address
    PORT = 44444        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        # c, addr = s.accept()     # Establish connection with client.
        # print ('Got connection from', addr)
        
        s.sendall(bytes("request" + dest_ip + " " + filename, 'utf-8'))
        
        print()
        print("Request for file successfully sent!")
        
        # print ('Got connection from', addr)
        print ("Receiving...")
        file_recv = s.recv(1024)
        while (file_recv):
            print ("Receiving...")
            fin.write(file_recv)
            file_recv = s.recv(1024)
            
    fin.close()
    
    print ("Successfully downloaded file: " + filename)
        

if __name__ == "__main__":
    main()
    


