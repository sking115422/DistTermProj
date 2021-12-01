# SBC Semi-Distributed Peer-to-Peer File Transfer

Please refer to the windows (master) branch for more information. Here were we will only go over how to run the project since it is different with linux/mac machines. 

## Running SBCFTP

Instructions for LINUX and MAC machines:

1. clone this repo to desired directory

2. open repository in terminal or IDE

2. cd into "DistTermProj/src"

3. run "chmod +x setup.sh" - this changes permissions so we can run setup.sh 

4. run "./setup.sh" - this will setup virtual environment and install depenedencies

5. Add files from your local machine into the newly created DistShared folder

7. run "chmod +x run_server.sh" - this changes permissions so we can run run_server.sh

8. run "./run_server.sh" - in the background, this starts the server on your machine and starts updating time stamp on the central server so it will know you are still active and online

9. If necessary, begin second terminal instance, else skip to step 11

10. cd into "DistTermProj/src" in new terminal

11. run "python3 client.py" - this allows you to request files from other nodes 

12. check "Downloads" directory to find you downloaded files 


NOTE: If you have to restart the server, you may get an error saying that process is already running. If this happens, do the following:

1. run "lsof -i :44444" - this shows python processes running on port 44444

2. run "kill -9 <process ids found above in 2> - this kill the old process completely

3. run "ps -ef | grep python" - to check if there are any other old python processes that might be running

4. kill any other old processes the same way as in 2 above 
