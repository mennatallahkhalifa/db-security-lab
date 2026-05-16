# 🔐 Database Security Lab — CN5134
**Ain Shams University | Faculty of Computer & Information Sciences**  
**Course: SEC304 — Spring 2026**

---

## 📋 Overview

This lab simulates **three real-world database vulnerabilities** in isolated Docker containers. Each vulnerability has its own application stack, exploit script, and flag.

> ⚠️ **For educational purposes only.** Run only in this isolated environment.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Attacker Machine                      │
│              (your browser / exploit script)             │
└────────────┬──────────────┬──────────────┬──────────────┘
             │              │              │
          :5001          :5002          :5003
             │              │              │
┌────────────▼───┐  ┌───────▼────────┐  ┌─▼──────────────┐
│  vuln1-flask   │  │  vuln2-flask   │  │  vuln3-flask   │
│  (Flask/Py)    │  │  (Flask/Py)    │  │  (Flask/Py)    │
└────────────┬───┘  └───────┬────────┘  └─┬──────────────┘
             │              │              │
┌────────────▼───┐  ┌───────▼────────┐  ┌─▼──────────────┐
│ vuln1-postgres │  │  vuln2-mysql   │  │  vuln3-mongo   │
│ PostgreSQL 12  │  │   MySQL 8.0    │  │  MongoDB 6.0   │
└────────────────┘  └────────────────┘  └────────────────┘
         │                   │                  │
         └───────────────────┴──────────────────┘
                     lab-network (bridge)
```

---

## 🎯 Vulnerabilities

| # | Vulnerability | CVE | Database | Port | Member |
|---|--------------|-----|----------|------|--------|
| 1 | PostgreSQL RCE via COPY TO PROGRAM | CVE-2019-9193 | PostgreSQL 12 | 5001 | Member 2 |
| 2 | Blind SQL Injection | CWE-89 | MySQL 8.0 | 5002 | Member 3 |
| 3 | NoSQL Operator Injection | CWE-943 | MongoDB 6.0 | 5003 | Member 4 |

---

## 🚀 Setup Instructions

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [Git](https://git-scm.com/) installed
- Ports 5001, 5002, 5003 free on your machine

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd db-security-lab
```

### 2. Start all containers
```bash
docker compose up --build
```

Wait until you see all services running. First build takes ~2-3 minutes.

### 3. Verify everything is up
```bash
docker compose ps
```

You should see **6 containers** all with status `Up`:
```
NAME                STATUS
vuln1-postgres      Up
vuln1-flask         Up
vuln2-mysql         Up
vuln2-flask         Up
vuln3-mongo         Up
vuln3-flask         Up
```

### 4. Access the apps
| Service | URL |
|---------|-----|
| Vuln 1 — PostgreSQL RCE | http://localhost:5001 |
| Vuln 2 — Blind SQLi | http://localhost:5002 |
| Vuln 3 — NoSQL Injection | http://localhost:5003 |

---

## 💥 Running the Exploits

Each vulnerability folder contains an exploit script:

```bash
# Exploit 1 — PostgreSQL RCE
python vuln1-postgresql/exploit.py

# Exploit 2 — Blind SQL Injection
python vuln2-blind-sqli/exploit.py

# Exploit 3 — NoSQL Injection
python vuln3-nosqli/exploit.py
```

---

## 🔍 Writeups

Each member wrote a detailed explanation of their vulnerability:

- `vuln1-postgresql/WRITEUP.md` — CVE-2019-9193 explained
- `vuln2-blind-sqli/WRITEUP.md` — Blind SQLi explained
- `vuln3-nosqli/WRITEUP.md` — NoSQL injection explained

---

## 🛑 Teardown

```bash
# Stop and remove all containers
docker compose down

# Also remove volumes (resets all databases)
docker compose down -v
```

---

## 👥 Team

| Member | Role |
|--------|------|
| Member 1 | Project Lead & Docker Integration |
| Member 2 | Vulnerability 1 — PostgreSQL RCE |
| Member 3 | Vulnerability 2 — Blind SQL Injection |
| Member 4 | Vulnerability 3 — NoSQL Injection |
| Member 5 | QA Testing & Penetration Testing Report |

---

## ⚠️ Troubleshooting

**Container keeps restarting?**
```bash
docker compose logs vuln1-app   # check logs for that service
```

**Port already in use?**
```bash
# Find and kill what's using the port (example for 5001)
lsof -i :5001
kill -9 <PID>
```

**MySQL not ready yet?**  
The Flask apps use `restart: on-failure` — they'll automatically reconnect once the DB is ready. Wait 30 seconds after `docker compose up`.

**Full reset:**
```bash
docker compose down -v
docker compose up --build
```
