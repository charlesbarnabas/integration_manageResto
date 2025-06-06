from ariadne import QueryType, MutationType
from database import get_db_connection
import sqlite3

query = QueryType()
mutation = MutationType()

@query.field("allUsers")
def resolve_all_users(_, info):
    conn = get_db_connection()
    try:
        users = conn.execute("SELECT id, name, email, role FROM users").fetchall()
        return [dict(user) for user in users]
    finally:
        conn.close()

@query.field("user")
def resolve_user(_, info, id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (id,)).fetchone()
        return dict(user) if user else None
    finally:
        conn.close()

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
        user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(user)
    except sqlite3.IntegrityError:
        conn.rollback()
        raise Exception(f"User dengan email '{input['email']}' sudah ada.")
    finally:
        conn.close()

@mutation.field("updateUser")
def resolve_update_user(_, info, input):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id FROM users WHERE id = ?", (input["id"],)).fetchone()
        if not user:
            raise Exception(f"User dengan ID {input['id']} tidak ditemukan.")
        conn.execute(
            "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?",
            (input["name"], input["email"], input.get("role"), input["id"])
        )
        conn.commit()
        updated_user = conn.execute("SELECT id, name, email, role FROM users WHERE id = ?", (input["id"],)).fetchone()
        return dict(updated_user)
    except sqlite3.IntegrityError:
        conn.rollback()
        raise Exception("Email sudah digunakan.")
    finally:
        conn.close()

@mutation.field("deleteUser")
def resolve_delete_user(_, info, id):
    conn = get_db_connection()
    try:
        user = conn.execute("SELECT id FROM users WHERE id = ?", (id,)).fetchone()
        if not user:
            raise Exception(f"User dengan ID {id} tidak ditemukan.")
        conn.execute("DELETE FROM users WHERE id = ?", (id,))
        conn.commit()
        return True
    finally:
        conn.close()

resolvers = [query, mutation]
