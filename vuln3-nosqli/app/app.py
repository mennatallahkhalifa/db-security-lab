# ============================================================
# Vulnerability 3 — NoSQL Injection (MongoDB)
# TODO: Member 4 replaces this file with their full implementation
# Attack: {"$gt": ""} bypasses login — flag is returned
# ============================================================

from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

app = Flask(__name__)

def get_db():
    client = MongoClient("mongodb://vuln3-db:27017/")
    return client["nosqlidb"]

@app.route("/")
def index():
    return "<h2>Vuln 3 — NoSQL Injection</h2><p>Member 4: replace this file with your implementation.</p>"

if __name__ == "__main__":
    time.sleep(5)  # Wait for MongoDB to be ready

    # Seed the database with a user and flag
    db = get_db()
    if db.users.count_documents({}) == 0:
        db.users.insert_one({
            "username": "admin",
            "password": "supersecret",
            "flag": "FLAG{nosql_operator_injection_auth_bypass}"
        })

    app.run(host="0.0.0.0", port=5003, debug=True)
