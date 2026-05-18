import os
import time
import psycopg2
from flask import Flask, request, render_template_string

print("DEBUG: app.py started", flush=True)

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "vuln1-db"),
    "user": os.environ.get("DB_USER", "postgres"),
    "password": os.environ.get("DB_PASS", "postgres"),
    "database": os.environ.get("DB_NAME", "labdb"),
}

HTML = """<!DOCTYPE html>
<html>
<head><title>PostgreSQL RCE Lab</title></head>
<body>
<h1>PostgreSQL CVE-2019-9193</h1>
<form action="/query" method="GET">
    <textarea name="q" rows="5" cols="80" placeholder="Enter any SQL..."></textarea><br>
    <input type="submit" value="Execute">
</form>
{% if query %}
<hr><b>Executed SQL:</b><br><pre>{{ query }}</pre>
<b>Result / Error:</b><br><pre>{{ result }}</pre>
{% endif %}
</body>
</html>
"""

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route("/")
def index():
    return render_template_string(HTML, query=None, result=None)

@app.route("/query")
def raw_query():
    q = request.args.get("q", "")
    result_text = ""
    try:
        conn = get_connection()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(q)
        try:
            rows = cur.fetchall()
            result_text = "\n".join(str(row) for row in rows) if rows else "(Query executed, no rows)"
        except psycopg2.ProgrammingError:
            result_text = "(Query executed successfully)"
        conn.close()
    except Exception as e:
        result_text = f"ERROR: {str(e)}"
    return render_template_string(HTML, query=q, result=result_text)

if __name__ == "__main__":
    print("DEBUG: inside main, waiting for DB...", flush=True)
    for attempt in range(30):
        try:
            conn = get_connection()
            conn.close()
            print(f"[+] Database ready after {attempt*2}s", flush=True)
            break
        except Exception as e:
            print(f"[-] Waiting for DB ({attempt+1}/30): {e}", flush=True)
            time.sleep(2)
    else:
        print("[!] Database not ready, but starting anyway...", flush=True)

    print("[*] Starting Flask server on 0.0.0.0:5001", flush=True)
    app.run(host="0.0.0.0", port=5001, debug=False)