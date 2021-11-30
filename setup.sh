rm -r venv

pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

echo ""
echo "SETUP COMPLETE"
echo ""