```bash
step 1 
cd user_service
python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt
pip install requests

atau
cd ..._service
.\venv\Scripts\Activate.ps1
python run.py

step 2
python init_db.py
python run.py
```

API User available at `http://localhost:5000`
API Menu available at `http://localhost:5001`
API Inventory available at `http://localhost:5002`
API Procurement available at `http://localhost:5003`
