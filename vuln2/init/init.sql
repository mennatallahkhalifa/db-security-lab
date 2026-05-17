-- Vulnerability 2: Blind SQL Injection
-- Member 3 fills in the full app logic

CREATE DATABASE IF NOT EXISTS logindb;
USE logindb;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(50)
);

-- Flag is hidden in a separate secrets table
CREATE TABLE IF NOT EXISTS secrets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flag VARCHAR(100)
);

INSERT INTO users (username, password) VALUES ('admin', 'password123');
INSERT INTO secrets (flag) VALUES ('FLAG{blind_sqli_extracted_char_by_char}');
