-- =============================================================
--  SecureBank CTF — MySQL 8.0 schema
--  Auto-executed by MySQL on first container start
--  (placed in /docker-entrypoint-initdb.d/)
-- =============================================================
CREATE DATABASE IF NOT EXISTS logindb;
USE logindb;


CREATE TABLE IF NOT EXISTS users (
    id       INT          AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50)  NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role     VARCHAR(20)  NOT NULL DEFAULT 'customer'
);

INSERT IGNORE INTO users (username, password, role) VALUES
    ('admin',   'Adm!n$uperSecure99',  'admin'),
    ('alice',   'alice_pass_2026',      'customer'),
    ('bob',     'b0bbyTables!',         'customer'),
    ('charlie', 'Ch@rlie123',           'customer');

-- Hidden flag table — attacker must extract this via blind SQLi
CREATE TABLE IF NOT EXISTS secrets (
    id   INT  AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(200) NOT NULL
);

INSERT IGNORE INTO secrets (id, flag) VALUES
    (1, 'FLAG{blind_sqli_char_by_char_exfil_success}');

-- Flavour data to make the app look realistic
CREATE TABLE IF NOT EXISTS transactions (
    id      INT          AUTO_INCREMENT PRIMARY KEY,
    user_id INT          NOT NULL,
    amount  DECIMAL(10,2) NOT NULL,
    note    VARCHAR(200),
    ts      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT IGNORE INTO transactions (user_id, amount, note) VALUES
    (2, -500.00,  'Transfer to savings'),
    (2,  1200.50, 'Payroll deposit'),
    (3, -75.00,   'Coffee shop'),
    (4,  300.00,  'Freelance payment');
