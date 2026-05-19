from flask import Flask, request, render_template_string, jsonify
from pymongo import MongoClient
import time
import json

app = Flask(__name__)

def get_db():
    client = MongoClient("mongodb://vuln3-db:27017/")
    return client["nosqlidb"]

HTML = """<!DOCTYPE html>
<html>
<head>
    <title>NoSQL Injection Lab</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .section {
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin: 15px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #555;
        }
        input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
            font-family: monospace;
        }
        textarea {
            resize: vertical;
            min-height: 80px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .result {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 4px solid #4CAF50;
            border-radius: 4px;
        }
        .error {
            border-left-color: #f44336;
        }
        pre {
            background-color: #282c34;
            color: #abb2bf;
            padding: 15px;
            border-radius: 4px;
            overflow-x: auto;
        }
        .hint {
            color: #666;
            font-size: 0.9em;
            font-style: italic;
            margin-top: 5px;
        }
        .overview {
            background-color: #fff3cd;
            padding: 15px;
            border-left: 4px solid #ffc107;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <h1> Vuln 3 — NoSQL Injection Lab</h1>
    
    <div class="overview">
        <h3>Overview:</h3>
        <p>Every one has a secret but some secrets if brought into light there is no coming back that would be <strong>THE END!!</strong></p>
        <p>Unleash your curiosity to find out what's hidden under the surface</p>
        
    </div>

    <!-- LOGIN SECTION -->
    <div class="section">
        <h2> Login</h2>
        <form id="loginForm">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" id="login_username" >
              
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="text" id="login_password" >
               
            </div>
            <button type="submit">Login</button>
        </form>
        <div id="loginResult"></div>
    </div>

    <!-- DOCUMENTS SECTION -->
    <div class="section">
        <h2> View My Documents</h2>
        <form id="documentsForm">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" id="doc_username" >
            </div>
            <button type="submit">Get Documents</button>
        </form>
        <div id="documentsResult"></div>
    </div>

    <!-- SEARCH SECTION -->
<div class="section">
    <h2> Search Documents</h2>

    <form id="searchForm">

        <div class="form-group">
            <label>Your Username:</label>

            <input
                type="text"
                id="search_username"
                
            >

            <div class="hint">
                Enter a valid username
            </div>
        </div>

        <div class="form-group">
            <label>Document Owner (filter):</label>

            <textarea
                id="search_doc_owner"
                
            ></textarea>

            <div class="hint">
                Search by owner name
            </div>
        </div>

        <button type="submit">
            Search
        </button>

    </form>

    <div id="searchResult"></div>
</div>

    <script>
        function parseJSON(str) {
            try {
                return JSON.parse(str);
            } catch(e) {
                return str;
            }
        }

        function displayResult(elementId, data, isError = false) {
            const el = document.getElementById(elementId);
            const resultClass = isError ? 'result error' : 'result';
            el.innerHTML = `<div class="${resultClass}"><pre>${JSON.stringify(data, null, 2)}</pre></div>`;
        }

        // Login Form
        document.getElementById('loginForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('login_username').value;
            const password = parseJSON(document.getElementById('login_password').value);
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, password})
                });
                const data = await response.json();
                displayResult('loginResult', data, !response.ok);
            } catch(err) {
                displayResult('loginResult', {error: err.message}, true);
            }
        });

        // Documents Form
        document.getElementById('documentsForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('doc_username').value;
            
            try {
                const response = await fetch('/documents', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username})
                });
                const data = await response.json();
                displayResult('documentsResult', data, !response.ok);
            } catch(err) {
                displayResult('documentsResult', {error: err.message}, true);
            }
        });

        // Search Form
        document.getElementById('searchForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('search_username').value;
            const doc_owner = parseJSON(document.getElementById('search_doc_owner').value);
            
            try {
                const response = await fetch('/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({username, doc_owner})
                });
                const data = await response.json();
                displayResult('searchResult', data, !response.ok);
            } catch(err) {
                displayResult('searchResult', {error: err.message}, true);
            }
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

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

@app.route("/documents", methods=["POST"])
def documents():
    data     = request.get_json(force=True)
    username = data.get("username")

    if not username:
        return jsonify({"error": "username required"}), 400

    db   = get_db()
    docs = list(db.documents.find(
        {"owner": username},
        {"_id": 0}
    ))
    return jsonify({"owner": username, "documents": docs})

@app.route("/search", methods=["POST"])
def search():
    data         = request.get_json(force=True)
    username     = data.get("username")
    doc_owner = data.get("doc_owner")

    if not username or not doc_owner:
        return jsonify({"error": "username and doc_owner required"}), 400

    db = get_db()

    # Quick check: username must exist
    user = db.users.find_one({"username": username}, {"_id": 0})
    if not user:
        return jsonify({"error": "unknown user"}), 403

    # !! VULNERABLE LINE — doc_owner can be an operator object !!
    docs = list(db.documents.find(
        {"owner": doc_owner},
        {"_id": 0}
    ))

    return jsonify({"results": docs})

if __name__ == "__main__":
    time.sleep(5)  # Wait for MongoDB to be ready

    db = get_db()   # ✅ FIX: define db FIRST

    # Initialize users
    if db.users.count_documents({}) == 0:
        db.users.insert_many([
            {"username": "admin", "password": "supersecret", "role": "admin"},
            {"username": "alice", "password": "alice123", "role": "employee"},
            {"username": "bob", "password": "bob456", "role": "employee"}
        ])

    # Initialize documents
    if db.documents.count_documents({}) == 0:
        db.documents.insert_many([
            {
                "owner": "admin",
                "title": "Q1 Budget Report",
                "content": "Total budget approved: $500,000."
            },
            {
                "owner": "alice",
                "title": "My Notes",
                "content": "Remember to submit timesheet by Friday."
            },
            {
                "owner": "bob",
                "title": "Project Plan",
                "content": "Phase 1 due end of month."
            },
            {
                "owner": "system",
                "title": "CONFIDENTIAL — Internal Credentials",
                "content": "FLAG{nosql_operator_I LOVE $$ <3}"
            }
        ])

    app.run(host="0.0.0.0", port=5003, debug=True)