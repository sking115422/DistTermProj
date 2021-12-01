rm -r venv

mkdir .\..\DistShared

mkdir .\..\Downloads

pip install virtualenv

virtualenv venv

call venv/Scripts/activate

pip install -r requirements.txt