# -------------------------------------------------------
#  vuln2 - Blind SQL Injection (MySQL 8.0 + Flask)
# -------------------------------------------------------
FROM python:3.11-slim

RUN pip install --no-cache-dir flask==3.0.3 pymysql==1.1.0 cryptography

WORKDIR /app
COPY src/ ./src/
COPY init/ ./init/

EXPOSE 5002
CMD ["python", "src/app.py"]
