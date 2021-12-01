

import mysql.connector
import os
from datetime import datetime as dt
import time as t
from pytz import timezone

try:

    db = mysql.connector.connect(
        host='173.230.133.41',
        user='user',
        password=''
    )

    print ()
    print (db)

    mycursor = db.cursor()
    
except:
    
    print ()
    print ("Could not connect to database...")


print()

try:
     
    now = None
    tz = timezone('EST')
    now = dt.now(tz)

    mycursor.execute ("USE CDS;")

    mycursor.execute ("SELECT COUNT(IP) FROM peer_list;")
    fetched = mycursor.fetchall()

    tot_entries = fetched[0][0]

    mycursor.execute("ALTER TABLE `peer_list` DROP `ID`;")
    mycursor.execute("ALTER TABLE `peer_list` AUTO_INCREMENT = 1;")
    mycursor.execute("ALTER TABLE `peer_list` ADD `ID` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")



    for x in range(tot_entries):
        y = x + 1
        mycursor.execute ("SELECT * FROM peer_list WHERE ID =" + str(y) + ";")
        each = mycursor.fetchall()
        
        print(each)
        
        diff_list = []
        ind = each [0][0]
        time_stamp = "NULL"
        time_stamp = each[0][3]
        print(time_stamp)
        
        if time_stamp == None:
            mycursor.execute ("DELETE FROM peer_list WHERE ID =" + str(y) + ";")
            db.commit()
            
            print ()
            print ("Entry " + str(ind) + " is NULL - deleted")
            print ()
            continue
        
        now_str = str(now)[:-6]
        
        time_stamp = dt.strptime(time_stamp, '%Y-%m-%d %H:%M:%S.%f')
        now_new = dt.strptime(now_str, '%Y-%m-%d %H:%M:%S.%f')
        
        print ("now " + str(now_new) + "  |  ts " + str(time_stamp))
        
        time_diff = now_new - time_stamp

        diff_list = str(time_diff).split(':')
        diff_sec = float (diff_list [1]) * 60 + float(diff_list[2])
        
        print ("diff_sec: " + str(diff_sec))
        
        try:
        
            tmp_list = []
            
            tmp_list = diff_list[0].split(" ")
            
            neg = tmp_list[0]
            
            print(neg)
            
        except:
            
            print("not negative value")
        
        if neg == "-1":
            
            print()
            print("Entry " + str(ind) + " is still active")
            print()
        
        elif diff_sec > 60:
            
            mycursor.execute ("DELETE FROM peer_list WHERE ID = " + str(ind) + ";")
            mycursor.execute ("ALTER TABLE peer_list AUTO_INCREMENT = 0;")
            
            db.commit()
            
            print()
            print ("Entry " + str(ind) + "timeout - deleted")
            print()
            
        else: 
            
            print()
            print("Entry " + str(ind) + " is still active")
            print()
            
except:
    
    print ()
    print ("File deletion failed...")