

from datetime import datetime as dt
import time as t
import mysql.connector
import argparse


#Argparse is used here to reading command line arguments
parser = argparse.ArgumentParser(description='To read in machine IP')

parser.add_argument('-ip', action='store', dest='M_IP', type=str, required=False, help='IP address that needs to be updated')

args = parser.parse_args()

machine_ip = args.M_IP

db = mysql.connector.connect(
    host='173.230.133.41',
    user='user',
    password=''
)

print ()
print (db)

mycursor = db.cursor()

while True:
    
    now = None
    now = dt.now()
    now = str (now)
    
    mycursor.execute ("USE CDS;")
    
    cmd = "UPDATE peer_list SET time_stamp = '" + now +  "' WHERE IP = '" + machine_ip + "';"
    print (cmd)
    
    mycursor.execute (cmd)
    
    print("Timestamp Updated:   " + now)
    
    db.commit()
    
    t.sleep(60)

