# 🍽️ Integration ManageResto

**Integration ManageResto** adalah platform manajemen restoran berbasis _microservices_ menggunakan Python Flask, GraphQL, dan Docker. Proyek ini bertujuan untuk mendemonstrasikan integrasi antar layanan REST/GraphQL dalam sistem restoran seperti manajemen user, menu, inventaris, transaksi, dan pengadaan.

---

## 🧱 Struktur Folder

```
integration_manageResto/
├── user_service/
├── menu_service/
├── inventory_service/
├── procurement_service/
├── transaction_service/
├── docker-compose.yml
└── README.md
```


---


## 🚀 Cara Menjalankan

### 🐳 Jalankan dengan Docker (Disarankan)

```bash
cd integration_manageResto
docker compose build && docker compose up -d
docker compose restart nginx # jika diperlukan
🖥️ Jalankan Secara Lokal (Tanpa Docker)
Lakukan untuk setiap service:

cd <nama_service>          # contoh: cd user_service
python -m venv venv        # buat virtual environment
source venv/bin/activate   # atau .\venv\Scripts\activate (Windows)
pip install -r requirements.txt
python run.py
Buka terminal baru dan jalankan service lainnya dengan cara yang sama.


🧪 Uji Pertama Kali
Jalankan user_service terlebih dahulu.
Buka browser ke: http://localhost:5000
Lakukan registrasi dan login sebagai user.
Setelah itu, eksplorasi fitur lainnya melalui antarmuka frontend atau via GraphQL Playground.


📡 API Endpoint
Layanan	Port
👤 User	http://localhost:5000
📋 Menu	http://localhost:5001
📦 Inventory	http://localhost:5002
🛒 Procurement	http://localhost:5003
💳 Transaction	http://localhost:5004


📌 Catatan
Setiap service berjalan secara independen.
GraphQL endpoint tersedia di /graphql (contoh: http://localhost:5000/graphql).
Semua data disimpan menggunakan SQLite secara default, dapat disesuaikan dengan PostgreSQL jika diperlukan.


---
