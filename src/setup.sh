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