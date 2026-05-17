# -------------------------------------------------------
#  vuln2 — Blind SQL Injection (MySQL 8.0 + Flask)
# -------------------------------------------------------
FROM python:3.11-slim

<<<<<<< HEAD
WORKDIR /app
COPY src/ .
=======
# Install pymysql (pure-Python MySQL driver — no system libs needed)
RUN pip install --no-cache-dir flask==3.0.3 pymysql==1.1.0
>>>>>>> 3806b4f03149070c185d161afda93ce1f9c044e1

WORKDIR /app
COPY src/    ./src/
COPY init/   ./init/

EXPOSE 5002
CMD ["python", "src/app.py"]
