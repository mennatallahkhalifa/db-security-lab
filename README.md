# Database Security Lab — CN5134
Ain Shams University | Faculty of Computer & Information Sciences
Course: SEC304 — Spring 2026

---

## Overview

This lab simulates three real-world database vulnerabilities in isolated Docker containers.
Each vulnerability has its own application stack, exploit script, and flag.

For educational purposes only. Run only in this isolated environment.

---

## Folder Structure

```
assignment1-vuln-lab/
├── docker-compose.yml
├── README.md
│
├── vuln1/                          # Vulnerability 1 — PostgreSQL RCE
│   ├── Dockerfile
│   ├── src/                        # Flask application source code
│   │   └── app.py
│   ├── init/                       # Database init scripts
│   │   └── init.sql
│   ├── config/                     # DB or app configuration files
│   └── solve/
│       ├── exploit.py              # Exploit script
│       └── WRITEUP.md              # Step-by-step walkthrough
│
├── vuln2/                          # Vulnerability 2 — Blind SQL Injection
│   ├── Dockerfile
│   ├── src/
│   │   └── app.py
│   ├── init/
│   │   └── init.sql
│   ├── config/
│   └── solve/
│       ├── exploit.py
│       └── WRITEUP.md
│
├── vuln3/                          # Vulnerability 3 — NoSQL Injection
│   ├── Dockerfile
│   ├── src/
│   │   └── app.py
│   ├── init/                       # Empty — MongoDB seeded from code
│   ├── config/
│   └── solve/
│       ├── exploit.py
│       └── WRITEUP.md
│
└── report/
    └── Assignment1_Report.pdf
```

---

## Architecture

```
+----------------------------------------------------------+
|                     Attacker Machine                     |
|               (browser / exploit script)                 |
+------------+---------------+--------------+--------------+
             |               |              |
          :5001           :5002          :5003
             |               |              |
+------------v----+  +-------v--------+  +-v--------------+
|   vuln1/src     |  |   vuln2/src    |  |   vuln3/src    |
|   Flask app     |  |   Flask app    |  |   Flask app    |
+------------+----+  +-------+--------+  +-+--------------+
             |               |              |
+------------v----+  +-------v--------+  +-v--------------+
| vuln1-postgres  |  |  vuln2-mysql   |  |  vuln3-mongo   |
| PostgreSQL 12   |  |  MySQL 8.0     |  |  MongoDB 6.0   |
+-----------------+  +----------------+  +----------------+
         |                   |                  |
         +-------------------+------------------+
                     lab-network (bridge)
```

---

## Vulnerabilities

| # | Vulnerability | CVE/CWE | Database | Port |
|---|--------------|---------|----------|------|
| 1 | PostgreSQL RCE via COPY TO PROGRAM | CVE-2019-9193 | PostgreSQL 12 | 5001 |
| 2 | Blind SQL Injection | CWE-89 | MySQL 8.0 | 5002 |
| 3 | NoSQL Operator Injection | CWE-943 | MongoDB 6.0 | 5003 |

---

## Setup Instructions

### Prerequisites
- Docker Desktop installed (https://www.docker.com/products/docker-desktop/)
- Git installed (https://git-scm.com/)
- Ports 5001, 5002, 5003 free on your machine
- Python 3 installed (for running exploit scripts)

### 1. Clone the repository
```bash
git clone https://github.com/mennatallahkhalifa/db-security-lab.git
cd db-security-lab
```

### 2. Start all containers
```bash
docker compose up --build
```

Wait until you see all services running. First build takes 2-3 minutes.

### 3. Verify everything is up
```bash
docker compose ps
```

You should see 6 containers all with status Up:
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

## Running the Exploits

```bash
# Exploit 1 — PostgreSQL RCE
python vuln1/solve/exploit.py

# Exploit 2 — Blind SQL Injection
python vuln2/solve/exploit.py

# Exploit 3 — NoSQL Injection
python vuln3/solve/exploit.py
```

---

## Writeups

Each vulnerability folder contains a detailed explanation:

- vuln1/solve/WRITEUP.md — CVE-2019-9193 explained
- vuln2/solve/WRITEUP.md — Blind SQLi explained
- vuln3/solve/WRITEUP.md — NoSQL injection explained

---

## Teardown

```bash
# Stop and remove all containers
docker compose down

# Also remove volumes (resets all databases)
docker compose down -v
```

---

## Troubleshooting

Container keeps restarting?
```bash
docker compose logs vuln1-flask
docker compose logs vuln2-flask
docker compose logs vuln3-flask
```

Port already in use?
```bash
# Windows
netstat -ano | findstr :5001

# Linux/Mac
lsof -i :5001
```

Database not ready yet?
The Flask apps use restart: on-failure so they reconnect automatically once the DB is ready. Wait 30 seconds after docker compose up.

Full reset:
```bash
docker compose down -v
docker compose up --build
```
