###SETUP SCRIPT

#Removes current virutal environment

#Makes two directories in the main project directory DistTermProj

#Makes sure pip3 is installed

#Creates virtual environment as venv

#Activates virutal environment

#Installs all project dependencies



rm -r venv

mkdir .\..\DistShared

mkdir .\..\Downloads

pip install virtualenv

virtualenv venv

call venv/Scripts/activate

pip install -r requirements.txt

echo.
echo SETUP COMPLETE
echo.