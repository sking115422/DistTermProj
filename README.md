# SBC Semi-Distributed Peer-to-Peer File Transfer

## Notes

* DistShared file needs to be placed in same file as the master folder for this code. 

* Downloads file need to be placed in the same fle as the master folder for this code. 

* Start by running the run_server.sh file. The will set up the server on your machine

* Run client.py when you want to download a file.

* SQL command to create new table in the database
USE CDS;
create table peer_list(
   ID INT NOT NULL AUTO_INCREMENT,
   IP VARCHAR(20) NOT NULL,
   filename VARCHAR(250) NOT NULL,
   time_stamp VARCHAR (250),
   PRIMARY KEY ( ID )
);