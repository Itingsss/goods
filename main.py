import sqlite3
from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Koneksi ke database SQLite
def connect_db():
    conn = sqlite3.connect('user_data.db')
    return conn

# Inisialisasi database dan membuat tabel jika belum ada
def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route untuk menambahkan pengguna baru
@app.route('/add-user', methods=['POST'])
def add_user():
    conn = connect_db()
    cursor = conn.cursor()

    # Ambil data dari request
    user_data = request.json
    username = user_data.get('username')
    password = user_data.get('password')

    # Hash password menggunakan SHA256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    try:
        # Tambahkan pengguna ke database
        cursor.execute('''
            INSERT INTO users (username, password)
            VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        
        # Mendapatkan ID pengguna yang baru ditambahkan
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        return jsonify({"message": "Username already exists"}), 409

    conn.close()
    # Hanya mengembalikan pesan sukses dan ID pengguna
    return jsonify({"message": "User added successfully", "user_id": user_id}), 201

# Route untuk autentikasi pengguna
@app.route('/auth', methods=['POST'])
def authenticate():
    conn = connect_db()
    cursor = conn.cursor()

    # Ambil data dari request
    auth_data = request.json
    username = auth_data.get('username')
    password = auth_data.get('password')

    # Hash password menggunakan SHA256
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password))
    user = cursor.fetchone()
    
    if user:
        return jsonify({"message": "Authentication successful"}), 200
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    init_db()
    app.run(debug=True)