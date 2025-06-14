import os

class Config:
    SECRET_KEY = 'user-secret-key'
    # Menggunakan path absolut ke folder instance
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(BASE_DIR, "instance", "user.db")}'
    # Menonaktifkan tracking modifications untuk mengurangi overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False 