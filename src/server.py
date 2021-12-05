

#IMPORT STATEMENTS

import socket
import mysql.connector
import os



###########################################################################################################
#HELPER FUNCTIONS


#function to connect with our MySQL database

#***YOU WILL NEED TO UPDATE THESE VALUES FOR YOUR OWN CENTRAL DATABASE***
def connect_to_db ():
    db = mysql.connector.connect(
        host='173.230.133.41',    #UPDATE
        user='user',    #UPDATE
        password=''    #UPDATE
    )

    print ()
    print (db)

    mycursor = db.cursor()
    
    return db, mycursor


#Function to return the local IP and hostname

def get_local_ip():
    
    local_ip_vm = None
    
    #For broadcast IP if avaliable/necessary 
    #Usually only nessary when virutal machines are involved
    
    try:
    
        os.system("hostname -I > hostname_i.txt")
        
        with open('hostname_i.txt') as f:
        
            tmp = str(f.readlines()[0])

        f.close()

        os.system("rm hostname_i.txt")

        tmplist = tmp.split(" ")

        for each in tmplist:
            
            #Making sure we get a 172 internal broadcast IP and not IP for loopback traffic
            if each [0:2] == '17' and each [0:2] != '127.0.0.1':    
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
    
    files = os.listdir('../DistShared')
    
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



##########################################################################################################################
#MAIN DRIVER FUNCTION FOR CLIENT

    
def main ():
    
    #Deleting all central db server entries that are assciated with this IP
    #There shouldnt be any, but just incase something strange happens this will avoid errors
    delete_files()
    
    #Pushing shared files to central db server
    push_to_server ()
    
    #Getting IP and Hostname of current machine
    host_ip, host_name = get_local_ip()
    
    #Designating filepath to text file that will store IP of current machine
    filepath = 'machine_ip.txt'

    #Removing file if it already exits
    if os.path.exists(filepath):
        os.system("rm " + filepath)
        
    #Creating file again
    os.system("touch " + filepath)
        
    #Writing machine IP to file we just created
    with open(filepath, 'w') as f:
        f.write(host_ip)       
        
    HOST = host_ip      #IP of current machine
    PORT = 44444      #Port to listen on (non-privileged ports are > 1023)

    #Outer loop to continuously listen for incoming requests
    while True:
        
        print ("###################################################")

        #Creating socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
            #Binding to IP and port
            s.bind((HOST, PORT))
            
            #Listeing for incoming requests
            s.listen()
            
            #Accepting connection
            conn, addr = s.accept()
            
            #Printing connection details
            print ()
            print('Connected: ', addr)
            
            with conn:
                
                file_to_send = ''
                
                #Inner loop 1 to keep connection open and receive file request
                while True:
                    
                    try:
                        
                        #Receiving file request
                        data = conn.recv(65536)
                        
                        #If no data is receive we close connection
                        if data == None:
                            print ()
                            print ("No request recieved")
                            break
                        
                        #Decoding request and spliting into list of parts
                        try:
                            data_str = data.decode('utf-8')
                            data_list = data_str.split(" ")
                        
                        #Throw exception if we cannot convert to ascii 
                        except:
                            print ()
                            print ("bytes are not covertible to ascii")
                        
                        #Checking to make sure it is a valid request
                        if data_list[0] == "request":
                
                            #Handling the case the file name requested has spaces in it
                            for z in range(2, len(data_list)):
                                file_to_send = file_to_send + " " + data_list[z]
                            
                            #Striping any extra white space from file name to ensure no errors occur
                            file_to_send = file_to_send.rstrip()
                            file_to_send = file_to_send.lstrip()
                        
                        #Opening file to send    
                        fo = open('../DistShared/' + file_to_send, 'rb')
                        
                        #Reading file
                        buf = fo.read(65536)

                        #Sending file until complete
                        while len(buf) != 0:
                            
                            conn.send(buf)
                            buf = fo.read(65536)
                            print ()
                            print ("Sending: " + file_to_send)
                        
                        #Close file and let user know whole file has been sent
                        fo.close()
                        print ("File sent!")
                    
                    #If error of some kind we just close connection so user can retry
                    except:
                        print ()
                        print ("Connection closed")
                        break
                    
                    
if __name__ == "__main__":
    main()
                        
                
            
                


