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

API user_service available at `http://localhost:5000`
API menu_service available at `http://localhost:5001`
API inventory_service available at `http://localhost:5002`
