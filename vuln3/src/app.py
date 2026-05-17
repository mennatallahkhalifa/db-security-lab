
from flask import Flask, request, jsonify
from pymongo import MongoClient
import time

app = Flask(__name__)



def get_db():
    client = MongoClient("mongodb://vuln3-db:27017/")
    return client["nosqlidb"]


@app.route("/")
def index():
    return """
    <h2>Vuln 3 — NoSQL Injection</h2>
  

    <p>
    Every one has a secret but some secrets if brought into  light there is no coming back that would be THE END!!
    </p>

    <p>
    Unleash your curiosity to find out what's hidden under the surface
    </p>
    <p>
    Over view:
    </p>
    <ul>
        <li>POST /login     — body: {username, password}</li>
        <li>GET  /documents — body: {username}  (your own docs)</li>
        <li>POST /search    — body: {username, filter_owner}</li>
    </ul>
    """



@app.route("/login", methods=["POST"])
def login():
    data     = request.get_json(force=True)
    username = data.get("username")   
    password = data.get("password")   
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    db = get_db()

    # VULNERABLE LINE
    user = db.users.find_one({"username": username, "password": password})

    if user:
        return jsonify({
            "message": f"Welcome, {user['username']}!",
            "role":    user["role"]
        })
    else:
        return jsonify({"error": "Invalid credentials."}), 401


# ── Normal endpoint — user sees only their own docs ──────────
@app.route("/documents", methods=["POST"])
def documents():
    data     = request.get_json(force=True)
    username = data.get("username")

    if not username:
        return jsonify({"error": "username required"}), 400

    db   = get_db()
    docs = list(db.documents.find(
        {"owner": username},
        {"_id": 0}          # _id: 0 hides MongoDB's internal ID field
    ))
    return jsonify({"owner": username, "documents": docs})



@app.route("/search", methods=["POST"])
def search():
    data         = request.get_json(force=True)
    username     = data.get("username")       # must be a known user
    doc_owner = data.get("doc_owner")   # attacker sends {"$ne": null}

    if not username or not doc_owner:
        return jsonify({"error": "username and doc_owner required"}), 400

    db = get_db()

    # Quick check: username must exist (loose gate — still bypassable)
    user = db.users.find_one({"username": username}, {"_id": 0})
    if not user:
        return jsonify({"error": "unknown user"}), 403

    # !! VULNERABLE LINE — doc_owner can be an operator object !!
    docs = list(db.documents.find(
        {"owner": doc_owner},
        {"_id": 0}          # _id: 0 hides MongoDB's internal ID field
    ))

    return jsonify({"results": docs})


if __name__ == "__main__":
    time.sleep(5)  # Wait for MongoDB to be ready

    db = get_db()

    #  users
    if db.users.count_documents({}) == 0:
        db.users.insert_many([
            {"username": "admin", "password": "supersecret", "role": "admin"},
            {"username": "alice", "password": "alice123",    "role": "employee"},
            {"username": "bob",   "password": "bob456",      "role": "employee"}
        ])


    if db.documents.count_documents({}) == 0:
        db.documents.insert_many([
            {"owner": "admin",  "title": "Q1 Budget Report",
             "content": "Total budget approved: $500,000."},
            {"owner": "alice",  "title": "My Notes",
             "content": "Remember to submit timesheet by Friday."},
            {"owner": "bob",    "title": "Project Plan",
             "content": "Phase 1 due end of month."},
            {
                # "system" is not a real login account.
                # Only reachable via $ne:null injection on /search.
                "owner":   "system",
                "title":   "CONFIDENTIAL — Internal Credentials",
                "content": "FLAG{nosql_operator_I LOVE $$ <3}"
            }
        ])

    app.run(host="0.0.0.0", port=5003, debug=True)