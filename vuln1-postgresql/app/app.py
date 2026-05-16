# ============================================================
# Vulnerability 1 — CVE-2019-9193: PostgreSQL COPY TO PROGRAM
# TODO: Member 2 replaces this file with their full implementation
# ============================================================

from flask import Flask, request, jsonify
import psycopg2
import time

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="vuln1-db",
        user="postgres",
        password="postgres",
        dbname="labdb"
    )

@app.route("/")
def index():
    return "<h2>Vuln 1 — PostgreSQL RCE (CVE-2019-9193)</h2><p>Member 2: replace this file with your implementation.</p>"

if __name__ == "__main__":
    time.sleep(5)  # Wait for DB to be ready
    app.run(host="0.0.0.0", port=5001, debug=True)
