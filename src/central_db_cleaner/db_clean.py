

#IMPORT STATEMENTS

import mysql.connector
from datetime import datetime as dt
from pytz import timezone



#DATABASE CLEANER SCRIPT

#Attempting to connect with our MySQL database

#***YOU WILL NEED TO UPDATE THESE VALUES FOR YOUR OWN CENTRAL DATABASE***
try:

    db = mysql.connector.connect(
        host='173.230.133.41',    #UPDATE
        user='user',    #UPDATE
        password=''    #UPDATE
    )

    print ()
    print (db)

    mycursor = db.cursor()
    
except:
    
    print ()
    print ("Could not connect to database...")


print()


#Attempting to delete old db entries
try:
     
    #Specifying easten timezone and taking current time
    now = None
    tz = timezone('EST')
    now = dt.now(tz)

    #Getting total number of db entries
    mycursor.execute ("USE CDS;")

    mycursor.execute ("SELECT COUNT(IP) FROM peer_list;")
    fetched = mycursor.fetchall()

    tot_entries = fetched[0][0]

    #Reordering index column ID so all numbers are consecutive starting from 1 and there are no gaps
    mycursor.execute("ALTER TABLE `peer_list` DROP `ID`;")
    mycursor.execute("ALTER TABLE `peer_list` AUTO_INCREMENT = 1;")
    mycursor.execute("ALTER TABLE `peer_list` ADD `ID` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;")


    #looping through all db entries
    for x in range(tot_entries):
        
        #Getting first entry
        y = x + 1
        mycursor.execute ("SELECT * FROM peer_list WHERE ID =" + str(y) + ";")
        each = mycursor.fetchall()
        
        print(each)
        
        #Parsing index (ID) and timestamp value of entry
        diff_list = []
        ind = each [0][0]
        time_stamp = "NULL"
        time_stamp = each[0][3]
        print(time_stamp)
        
        #If entry does not have a time stamp for some reason delete it
        if time_stamp == None:
            mycursor.execute ("DELETE FROM peer_list WHERE ID =" + str(y) + ";")
            db.commit()
            
            print ()
            print ("Entry " + str(ind) + " is NULL - deleted")
            print ()
            continue
        
        #Making current timestamp we got earlier into a string and striping extraneous data
        now_str = str(now)[:-6]
        
        #Changing current timestamp and entry timestamp into a similar format so we can find their difference 
        time_stamp = dt.strptime(time_stamp, '%Y-%m-%d %H:%M:%S.%f')
        now_new = dt.strptime(now_str, '%Y-%m-%d %H:%M:%S.%f')
        
        print ("now " + str(now_new) + "  |  ts " + str(time_stamp))
        
        #Finding difference between current time and time associated with entry
        time_diff = now_new - time_stamp

        #Parsing difference into list of parts
        diff_list = str(time_diff).split(':')
        
        #Calculating the time difference in seconds
        diff_sec = float (diff_list [1]) * 60 + float(diff_list[2])
        
        print ("diff_sec: " + str(diff_sec))
        
        #Checking to see if the difference is negative
        try:
        
            tmp_list = []
            tmp_list = diff_list[0].split(" ")
            neg = tmp_list[0]
            print(neg)
            
        except:
            
            print("not negative value")
            
        #If difference is negative we know entry is still valid
        if neg == "-1":
            
            print()
            print("Entry " + str(ind) + " is still active")
            print()
        
        #If difference is greater that 60 seconds we assume peer is inactive and delete its associated entries
        elif diff_sec > 60:
            
            mycursor.execute ("DELETE FROM peer_list WHERE ID = " + str(ind) + ";")
            mycursor.execute ("ALTER TABLE peer_list AUTO_INCREMENT = 0;")
            
            db.commit()
            
            print()
            print ("Entry " + str(ind) + "timeout - deleted")
            print()
        
        #If difference is less that 60 and not negative that is also valid
        else: 
            
            print()
            print("Entry " + str(ind) + " is still active")
            print()
            
#Letting db admin know something failed
except:
    
    print ()
    print ("File deletion failed...")