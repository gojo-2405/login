from flask import Flask, request, jsonify, send_from_directory
import pymysql
import bcrypt
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)

# DB connection
conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASS"),
    database=os.getenv("DB_NAME"),
    cursorclass=pymysql.cursors.DictCursor
)

# Serve main page
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

# Serve success pages
@app.route("/login-success")
def login_success():
    return send_from_directory('.', 'login_success.html')

@app.route("/signup-success")
def signup_success():
    return send_from_directory('.', 'signup_success.html')


# 🔐 Signup
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"message": "All fields required"}), 400

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    if cursor.fetchone():
        return jsonify({"message": "User already exists"}), 409

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hashed_pw.decode())
    )
    conn.commit()

    return jsonify({"message": "Signup successful"}), 201


# 🔑 Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()

    if result:
        if bcrypt.checkpw(password.encode(), result["password"].encode()):
            return jsonify({"message": "Login successful"}), 200

    return jsonify({"message": "Invalid credentials"}), 401


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
