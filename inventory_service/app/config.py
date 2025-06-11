class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Procurement service URL
    PROCUREMENT_SERVICE_URL = 'http://localhost:5003/api/procurement'  # Example URL, adjust as needed
