DROP DATABASE IF EXISTS project;

CREATE DATABASE project;
USE project;

CREATE TABLE owner(
    account_id INT(8) NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
    CONSTRAINT owner_password_valid
    CHECK (
        (INSTR(password, '0') > 0) OR
        (INSTR(password, '1') > 0) OR
        (INSTR(password, '2') > 0) OR
        (INSTR(password, '3') > 0) OR
        (INSTR(password, '4') > 0) OR
        (INSTR(password, '5') > 0) OR
        (INSTR(password, '6') > 0) OR
        (INSTR(password, '7') > 0) OR
        (INSTR(password, '8') > 0) OR
        (INSTR(password, '9') > 0)
    ),
	email VARCHAR(50) NOT NULL,
    CONSTRAINT owner_email_valid CHECK (email LIKE '%_%@%_%.%_%'),
	CONSTRAINT owner_email_uk UNIQUE(email),
	PRIMARY KEY(account_id) 
);

CREATE TABLE customer(
    account_id INT(8) NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
    CONSTRAINT customer_password_valid
    CHECK (
        (INSTR(password, '0') > 0) OR
        (INSTR(password, '1') > 0) OR
        (INSTR(password, '2') > 0) OR
        (INSTR(password, '3') > 0) OR
        (INSTR(password, '4') > 0) OR
        (INSTR(password, '5') > 0) OR
        (INSTR(password, '6') > 0) OR
        (INSTR(password, '7') > 0) OR
        (INSTR(password, '8') > 0) OR
        (INSTR(password, '9') > 0)
    ),
	email VARCHAR(50) NOT NULL,
    CONSTRAINT customer_email_valid CHECK (email LIKE '%_%@%_%.%_%'),
	CONSTRAINT customer_email_uk UNIQUE(email),
	PRIMARY KEY(account_id) 
);

-- TEST DATA
-- error
-- INSERT INTO customer VALUES(1, "customer", "password", "customer"); 
--valid
INSERT INTO customer VALUES(1, "customer", "p1", "customer@gugol.kom"); 