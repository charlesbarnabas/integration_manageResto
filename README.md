```bash
step 1 
cd user_service
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

step 2
python init_db.py
python app.py
```

API available at `http://localhost:5000`
