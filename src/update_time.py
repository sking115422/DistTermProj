

#IMPORT STATEMENTS

from datetime import datetime as dt
import time as t
import mysql.connector
from pytz import timezone



#DATABASE TIMESTAMP UPDATER SCRIPT

#Allows time for the peer server to push files to the central server (MySQL DB) before updating timestamps
t.sleep (2)

#Getting current machine IP address from file where it is stored
with open('machine_ip.txt') as f:
    machine_ip = str(f.readlines()[0])

#Connecting to MySQL database

#***YOU WILL NEED TO UPDATE THESE VALUES FOR YOUR OWN CENTRAL DATABASE***
db = mysql.connector.connect(
    host='173.230.133.41',    #UPDATE
    user='user',    #UPDATE
    password=''    #UPDATE
)

mycursor = db.cursor()


print ("update_time.py is running")

#Loop to continually update time stamp until program is killed or machine is shutdown
while True:
    
    #Specifying easten timezone and taking current time
    #Putting current time in compatible timestamp format
    now = None
    tz = timezone('EST')
    now = dt.now(tz)
    now = now.strftime("%Y-%m-%d %H:%M:%S.%f")
    
    #Updating all timestamps associate with our machine's IP
    mycursor.execute ("USE CDS;")
    cmd = "UPDATE peer_list SET time_stamp = '" + now +  "' WHERE IP = '" + machine_ip + "';"
    mycursor.execute (cmd)
    print("Timestamp Updated:   " + now)
    db.commit()
    
    #Waiting 15 seconds to update again
    t.sleep(15)

