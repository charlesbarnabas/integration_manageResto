from app import create_app, db
from app.models import User
from app import bcrypt

def init_db():
    app = create_app()
    with app.app_context():
        # Buat semua tabel
        db.create_all()
        
        # Cek apakah sudah ada user
        if not User.query.first():
            # Buat user default
            hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
            admin = User(username='admin', password=hashed_password)
            db.session.add(admin)
            db.session.commit()
            print("User default berhasil dibuat!")

if __name__ == '__main__':
    init_db() 