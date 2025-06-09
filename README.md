```bash
step 1 
cd user_service
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
pip install requests
step 2
python init_db.py
python run.py
```

API User available at `http://localhost:5000`
API Menu available at `http://localhost:5001`
API Inventory available at `http://localhost:5002`
API Procurement available at `http://localhost:5003`
