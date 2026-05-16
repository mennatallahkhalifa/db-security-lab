# ============================================================
# Vulnerability 2 — Blind SQL Injection
# TODO: Member 3 replaces this file with their full implementation
# ============================================================

from flask import Flask, request, jsonify
import mysql.connector
import time

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host="vuln2-db",
        user="root",
        password="root",
        database="logindb"
    )

@app.route("/")
def index():
    return "<h2>Vuln 2 — Blind SQL Injection</h2><p>Member 3: replace this file with your implementation.</p>"

if __name__ == "__main__":
    time.sleep(10)  # Wait for MySQL to be ready
    app.run(host="0.0.0.0", port=5002, debug=True)
