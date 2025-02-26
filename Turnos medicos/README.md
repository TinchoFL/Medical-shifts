
## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
pip install flask-SQLAlchemy
pip install flask-cors
```

## Run

```bash
sudo systemctl start postgresql

source venv/bin/activate
cd backend
python3 main.py

cd ../frontend
python3 -m http.server


```
