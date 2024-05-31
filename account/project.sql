DROP DATABASE IF EXISTS project;

CREATE OR REPLACE USER 'project'@'localhost' IDENTIFIED BY 'ilove127';
CREATE DATABASE project;
GRANT ALL ON scott.* TO 'project'@'localhost';

USE project;

CREATE TABLE customer(
    account_id INT(8) NOT NULL AUTO_INCREMENT,
	name VARCHAR(50) NOT NULL,
	password VARCHAR(50) NOT NULL,
    CONSTRAINT customer_password_valid CHECK (password LIKE '%[0-9]%'),
	email VARCHAR(50) NOT NULL,
    CONSTRAINT customer_email_valid CHECK (email LIKE '%@%.%'),
	CONSTRAINT customer_email_uk UNIQUE(email),
	PRIMARY KEY(account_id) 
);

-- TEST DATA
-- error
INSERT INTO customer VALUES(1, "customer", "password", "customer"); 
--valid
INSERT INTO customer VALUES(1, "customer", "password", "customer@gugol.kom"); 