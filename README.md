# SBC Semi-Distributed Peer-to-Peer File Transfer

Please refer to the windows (master) branch for more information. Here were we will only go over how to run the project since it is different with linux/mac machines. 

## Running SBCFTP

Instructions for LINUX and MAC machines:

1. clone this repo to desired directory

2. in the "DistTermProj" directory, create 2 files called "DistShared" and "Downloads"

3. upload files you wish to share into the "DistShared" file you just made 

4. cd into "DistTermProj/src"

5. run "./setup.sh" - this will setup virtual environment and install depenedencies

6. run "./run_server.sh" - this starts the server on your machine and starts updating time stamp on the central server so it will know you are still active and online

8. run "python client.py" - this allows you to request files from other nodes 

9. check "Downloads" directory to find you downloaded files 
