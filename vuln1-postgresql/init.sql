-- Vulnerability 1: PostgreSQL RCE via COPY TO PROGRAM (CVE-2019-9193)
-- Member 2 fills in the full app logic

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

INSERT INTO users (username, password) VALUES
('admin', 'admin123'),
('alice', 'password1');

-- The flag is in the OS filesystem (/flag.txt), not the DB
-- It gets captured via COPY TO PROGRAM OS command execution
