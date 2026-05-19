import os
import time
import psycopg2
from flask import Flask, request, render_template_string

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "vuln1-db"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "postgres"),
    "database": os.environ.get("DB_NAME", "labdb"),
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PostgreSQL RCE Lab | CVE-2019-9193</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', 'Inter', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            min-height: 100vh;
            padding: 2rem;
            color: #e0e0e0;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .card {
            background: rgba(30, 30, 46, 0.7);
            backdrop-filter: blur(12px);
            border-radius: 28px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease;
        }
        .card:hover {
            transform: translateY(-4px);
        }
        h1 {
            font-size: 1.8rem;
            font-weight: 600;
            background: linear-gradient(135deg, #c084fc, #60a5fa);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            margin-bottom: 0.5rem;
        }
        .badge {
            display: inline-block;
            background: #f43f5e;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 999px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 1rem;
            vertical-align: middle;
        }
        .sub {
            color: #94a3b8;
            margin-bottom: 1.5rem;
            border-left: 3px solid #f43f5e;
            padding-left: 1rem;
        }
        textarea {
            width: 100%;
            background: #1e1e2e;
            border: 1px solid #334155;
            border-radius: 16px;
            padding: 1rem;
            color: #f1f5f9;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
            font-size: 0.9rem;
            resize: vertical;
            transition: 0.2s;
        }
        textarea:focus {
            outline: none;
            border-color: #c084fc;
            box-shadow: 0 0 0 3px rgba(192, 132, 252, 0.3);
        }
        button {
            background: linear-gradient(90deg, #c084fc, #60a5fa);
            border: none;
            padding: 0.75rem 2rem;
            border-radius: 40px;
            font-weight: 600;
            color: white;
            cursor: pointer;
            transition: 0.2s;
            margin-top: 1rem;
            font-size: 1rem;
        }
        button:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(192, 132, 252, 0.4);
        }
        .result-box {
            background: #0f0f1a;
            border-radius: 20px;
            padding: 1.25rem;
            margin-top: 1.5rem;
            border-left: 5px solid #c084fc;
            overflow-x: auto;
        }
        .result-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
            color: #c084fc;
            margin-bottom: 0.5rem;
        }
        pre {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
            word-break: break-word;
            color: #d9e0ee;
            margin: 0;
        }
        .error {
            border-left-color: #f43f5e;
        }
        .error .result-label {
            color: #f43f5e;
        }
        .footer {
            text-align: center;
            margin-top: 2rem;
            font-size: 0.75rem;
            color: #475569;
        }
        @media (max-width: 640px) {
            body { padding: 1rem; }
            .card { padding: 1.25rem; }
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <h1>🐘 PostgreSQL RCE <span class="badge">CVE-2019-9193</span></h1>
        <div class="sub">COPY TO PROGRAM — superuser command execution</div>
        <form method="GET" action="/query">
            <textarea name="q" rows="6" placeholder="Enter any SQL query…&#10;Example: SELECT version();&#10;COPY (SELECT '') TO PROGRAM 'id';"></textarea>
            <div style="display: flex; justify-content: flex-end;">
                <button type="submit">🚀 Execute Query</button>
            </div>
        </form>
    </div>

    {% if query %}
    <div class="card">
        <div class="result-box">
            <div class="result-label">📋 Executed SQL</div>
            <pre>{{ query }}</pre>
        </div>
        <div class="result-box {% if error %}error{% endif %}">
            <div class="result-label">{% if error %}⚠️ Error{% else %}✅ Result{% endif %}</div>
            <pre>{{ result }}</pre>
        </div>
    </div>
    {% endif %}

    <div class="footer">
        🔐 Educational CTF lab — PostgreSQL 12.0 (vulnerable) | Superuser connection | Flag at /tmp/flag.txt
    </div>
</div>
</body>
</html>
"""

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template_string(HTML, query=None, result=None, error=False)

@app.route("/query")
def raw_query():
    q = request.args.get("q", "")
    result_text = ""
    error = False
    try:
        conn = get_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(q)
        try:
            rows = cur.fetchall()
            result_text = "\n".join(str(row) for row in rows) if rows else "(Query executed, no rows returned)"
        except psycopg2.ProgrammingError:
            result_text = "(Query executed successfully – no result set)"
        conn.close()
    except Exception as e:
        result_text = str(e)
        error = True
    return render_template_string(HTML, query=q, result=result_text, error=error)

if __name__ == "__main__":
    print("🚀 Starting PostgreSQL RCE Lab...", flush=True)
    for attempt in range(30):
        try:
            conn = get_connection()
            conn.close()
            print(f"✅ Database ready after {attempt*2}s", flush=True)
            break
        except Exception as e:
            print(f"⏳ Waiting for DB ({attempt+1}/30): {e}", flush=True)
            time.sleep(2)
    else:
        print("⚠️ Database not ready, but starting anyway...", flush=True)
    app.run(host="0.0.0.0", port=5001, debug=False)