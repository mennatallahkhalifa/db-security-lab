# -------------------------------------------------------
#  vuln2 — Blind SQL Injection (MySQL 8.0 + Flask)
# -------------------------------------------------------
FROM python:3.11-slim

# Install pymysql (pure-Python MySQL driver — no system libs needed)
RUN pip install --no-cache-dir flask==3.0.3 pymysql==1.1.0

WORKDIR /app
COPY src/    ./src/
COPY init/   ./init/

EXPOSE 5000

CMD ["python", "/app/src/app.py"]
