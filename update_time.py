

from datetime import datetime as dt
import time as t
import mysql.connector
from pytz import timezone

t.sleep (3)

with open('machine_ip.txt') as f:
    machine_ip = str(f.readlines()[0])

db = mysql.connector.connect(
    host='173.230.133.41',
    user='user',
    password=''
)

mycursor = db.cursor()

print ("update_time.py is running")

while True:
    
    now = None
    tz = timezone('EST')
    now = dt.now(tz)
    now = now.strftime("%Y-%m-%d %H:%M%S.%f")
    
    mycursor.execute ("USE CDS;")
    
    cmd = "UPDATE peer_list SET time_stamp = '" + now +  "' WHERE IP = '" + machine_ip + "';"
    # print (cmd)
    
    mycursor.execute (cmd)
    
    print("Timestamp Updated:   " + now)
    
    db.commit()
    
    t.sleep(15)

