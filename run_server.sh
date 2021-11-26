rm -r venv

pip install virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

python3 server.py & python3 update_time.py

