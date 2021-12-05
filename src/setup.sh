###SETUP SCRIPT

#Removes current virutal environment

#Makes two directories in the main project directory DistTermProj

#Makes sure pip3 is installed

#Creates virtual environment as venv

#Activates virutal environment

#Installs all project dependencies

rm -r venv

mkdir ../DistShared

mkdir ../Downloads

pip3 install virtualenv

virtualenv venv

source venv/bin/activate

pip3 install -r requirements.txt

echo ""
echo "SETUP COMPLETE"
echo ""