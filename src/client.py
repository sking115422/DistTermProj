

#IMPORT STATEMENTS

import socket
import mysql.connector
import time



###########################################################################################################
#HELPER FUNCTIONS


#Function to connect with our MySQL database

#***YOU WILL NEED TO UPDATE THESE VALUES FOR YOUR OWN CENTRAL DATABASE***
def connect_to_db ():
    db = mysql.connector.connect(
        host='173.230.133.41',   #UPDATE
        user='user',    #UPDATE
        password=''    #UPDATE
    )

    print ()
    print (db)

    mycursor = db.cursor()
    
    return db, mycursor
        

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



##########################################################################################################################
#MAIN DRIVER FUNCTION FOR CLIENT


def main():
    
    #Pulling down all central server entries' IP and filename as a list of pairs 
    pairlist = pull_from_server ()
    
    #Getting user input for index of file they wish to download
    print ()
    print ("Please enter the index number of the file you wish to download!")
    fileindex = int(input())
    
    #Storing appropriate IP and filename that correspond to user's entry
    dest_ip = pairlist [fileindex - 1][0]
    filename = pairlist [fileindex - 1][1]
    
    #Ask for user input to confirm their file request selection
    print ()
    print ("You are asking for file: " + filename + " from IP address: " + dest_ip + ". Correct? (Y/n)")
    proceed = input()
    
    #Terminating program if user accidentally made wrong selection
    if proceed == 'n' or proceed == 'N':
        print("Program terminating...")
        exit()
    
    #Creating and opening filename of requested file so we can write to it later
    fin = open("../Downloads/" + filename, "wb")
        
    HOST = dest_ip  # The server's hostname or IP address
    PORT = 44444   # The port used by the server arbitrarily chosen (must be greater than 1024 as these are restricted)

    #Creating socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.settimeout(3)         #Setting socket timeout to be 3 seconds
        s.connect((HOST, PORT))     #Connecting to peer server on HOST and PORT above
        
        print ()
        print ("Connected successfully")
        
        #Grabing timestamp before we send request
        start_time = time.time()
        
        #Sending request to server
        s.sendall(bytes("request " + dest_ip + " " + filename, 'utf-8'))
        
        print()
        print("Request for file successfully sent!")

        #Receiving server response
        file_recv = s.recv(65536)   #65536 is maximum buffer size
        
        #Continue receiving bytes from server until file is completed downloaded
        while True:
            print ("Receiving")
            fin.write(file_recv)
            try:
                file_recv = s.recv(65536)
            except:
                print("All bytes received")
                break
        
        #Grab timestamp after fill finished downloading and calculating total download latency
        end_time = time.time()
        exec_time = end_time - start_time - 3   #subtracting socket socket time out from latency
        
        #Printing latency for user
        print()
        print ("File download time: ", exec_time)
        
    #Closing file
    fin.close()
    
    #Alerting user of successful download
    print ()
    print ("Successfully downloaded file: " + filename + " !")
    print ()

if __name__ == "__main__":
    main()
    


