from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ariadne import QueryType, MutationType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
import sqlite3

# Fungsi koneksi DB
def get_db_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

# Inisialisasi DB (jalankan sekali di awal)
def init_db():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        role TEXT
    )
    """)
    conn.commit()
    conn.close()

# Load schema GraphQL
type_defs = load_schema_from_path("schema.graphql")

query = QueryType()
mutation = MutationType()

@query.field("allUsers")
def resolve_all_users(_, info):
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return [dict(row) for row in users]

@query.field("user")
def resolve_user(_, info, id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    conn.close()
    return dict(user) if user else None

@mutation.field("createUser")
def resolve_create_user(_, info, input):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (name, email, role) VALUES (?, ?, ?)",
            (input["name"], input["email"], input.get("role"))
        )
        conn.commit()
        user_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
        user = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user)
    except sqlite3.IntegrityError:
        raise Exception("Email sudah digunakan.")
    finally:
        conn.close()

@mutation.field("updateUser")
def resolve_update_user(_, info, input):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (input["id"],)).fetchone()
    if not user:
        raise Exception(f"User dengan ID {input['id']} tidak ditemukan.")
    try:
        conn.execute(
            "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?",
            (input["name"], input["email"], input.get("role"), input["id"])
        )
        conn.commit()
        updated_user = conn.execute("SELECT * FROM users WHERE id = ?", (input["id"],)).fetchone()
        return dict(updated_user)
    except sqlite3.IntegrityError:
        raise Exception("Email sudah digunakan.")
    finally:
        conn.close()

@mutation.field("deleteUser")
def resolve_delete_user(_, info, id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
    if not user:
        raise Exception(f"User dengan ID {id} tidak ditemukan.")
    conn.execute("DELETE FROM users WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return True

# Buat schema
schema = make_executable_schema(type_defs, [query, mutation])

# Inisialisasi FastAPI dan GraphQL
app = FastAPI()
app.add_route("/graphql", GraphQL(schema, debug=True))

# Jalankan init DB saat container start
init_db()
