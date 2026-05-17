from flask import Flask, request, render_template_string
import pymysql
import os
import time

app = Flask(__name__)

DB_CONFIG = {
    "host":     os.environ.get("DB_HOST",     "vuln2-mysql"),
    "user":     os.environ.get("DB_USER",     "ctfuser"),
    "password": os.environ.get("DB_PASSWORD", "ctfpass"),
    "database": os.environ.get("DB_NAME",     "ctfdb"),
    "port":     int(os.environ.get("DB_PORT", 3306)),
}

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>SecureBank Login</title>
  <style>
    body { font-family: Arial, sans-serif; background: #1a1a2e; color: #eee;
           display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
    .box { background: #16213e; padding: 40px; border-radius: 10px;
           box-shadow: 0 0 20px rgba(0,150,255,0.2); width: 320px; }
    h2 { text-align: center; color: #00b4d8; margin-bottom: 30px; }
    input { width: 100%; padding: 10px; margin: 8px 0; background: #0f3460;
            border: 1px solid #00b4d8; border-radius: 5px; color: #eee;
            box-sizing: border-box; }
    button { width: 100%; padding: 12px; background: #00b4d8; border: none;
             border-radius: 5px; color: #000; font-weight: bold; cursor: pointer; margin-top: 10px; }
    button:hover { background: #0096c7; }
    .msg { text-align: center; margin-top: 15px; padding: 10px;
           border-radius: 5px; font-weight: bold; }
    .success { background: #1b4332; color: #52b788; border: 1px solid #52b788; }
    .error   { background: #3b0a0a; color: #e63946; border: 1px solid #e63946; }
  </style>
</head>
<body>
  <div class="box">
    <h2>🏦 SecureBank</h2>
    <form method="POST">
      <input type="text"     name="username" placeholder="Username" autocomplete="off" />
      <input type="password" name="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>
    {% if message %}
      <div class="msg {{ css_class }}">{{ message }}</div>
    {% endif %}
  </div>
</body>
</html>
"""

def get_db():
    return pymysql.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def login():
    message  = None
    css_class = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            conn   = get_db()
            cursor = conn.cursor()

            # !! INTENTIONALLY VULNERABLE — NO SANITISATION !!
            query = (
                f"SELECT * FROM users "
                f"WHERE username = '{username}' AND password = '{password}'"
            )
            cursor.execute(query)
            row = cursor.fetchone()
            cursor.close()
            conn.close()

            if row:
                message   = f"Welcome back, {row[1]}! Login successful."
                css_class = "success"
            else:
                message   = "Invalid credentials. Access denied."
                css_class = "error"

        except Exception:
            message   = "Invalid credentials. Access denied."
            css_class = "error"

    return render_template_string(LOGIN_HTML, message=message, css_class=css_class)


@app.route("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return "OK", 200
    except Exception:
        return "DB not ready", 503


if __name__ == "__main__":
    # Wait for MySQL to be ready before starting
    for i in range(30):
        try:
            conn = get_db()
            conn.close()
            print("[+] Database connected.")
            break
        except Exception as e:
            print(f"[*] Waiting for database... ({i+1}/30)")
            time.sleep(2)

    app.run(host="0.0.0.0", port=5000, debug=False)
