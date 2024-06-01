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

CREATE TABLE food_establishment(
    establishment_id INT(8) NOT NULL AUTO_INCREMENT,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    average_rating INT(2),
    name VARCHAR(50) NOT NULL,
    account_id INT(8) NOT NULL,
    PRIMARY KEY(establishment_id),
    CONSTRAINT food_establishment_account_id_fk FOREIGN KEY(account_id) REFERENCES owner(account_id)
);

-- TEST DATA --

-- Customer insertion

-- bad email format
INSERT INTO customer VALUES(1, "customer", "password", "customer@gugol.kom");

-- bad password format
INSERT INTO customer VALUES(1, "customer", "password1", "customer"); 

-- valid
INSERT INTO customer VALUES(1, "customer", "password1", "customer@gugol.kom");

-- Owner insertion

-- bad password format
-- INSERT INTO owner VALUES(1, "owner", "password", "customer@gugol.kom");

-- bad email format
-- INSERT INTO owner VALUES(1, "owner", "password1", "customer");

-- valid
INSERT INTO owner VALUES(1, "owner", "password1", "customer@gugol.kom");

-- Food establishment insertion

-- account id does not exist
INSERT INTO food_establishment VALUES(1, "location", "description", 5, "name", 2);

-- valid
INSERT INTO food_establishment VALUES(1, "location", "description", 5, "name", 1);
INSERT INTO food_establishment(location, description, average_rating, name, account_id) VALUES("location", "description", 5, "name", 1);
