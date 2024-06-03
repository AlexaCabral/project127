DROP DATABASE IF EXISTS project;

CREATE DATABASE project;

USE project;

CREATE TABLE owner(
    account_id INT(8) NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    CONSTRAINT owner_password_valid CHECK (password REGEXP '[0-9]'),
    email VARCHAR(50) NOT NULL,
    CONSTRAINT owner_email_valid CHECK (email LIKE '%_%@%_%.%_%'),
    CONSTRAINT owner_email_uk UNIQUE(email),
    PRIMARY KEY(account_id)
);

CREATE TABLE customer(
    account_id INT(8) NOT NULL AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,
    CONSTRAINT customer_password_valid CHECK (password REGEXP '[0-9]'),
    email VARCHAR(50) NOT NULL,
    CONSTRAINT customer_email_valid CHECK (email LIKE '%_%@%_%.%_%'),
    CONSTRAINT customer_email_uk UNIQUE(email),
    PRIMARY KEY(account_id)
);

CREATE TABLE food_establishment(
    establishment_id INT(8) NOT NULL AUTO_INCREMENT,
    location VARCHAR(100) NOT NULL,
    description TEXT,
    average_rating DECIMAL,
    name VARCHAR(50) NOT NULL,
    account_id INT(8) NOT NULL,
    PRIMARY KEY(establishment_id),
    CONSTRAINT food_establishment_account_id_fk FOREIGN KEY(account_id) REFERENCES owner(account_id)
);

CREATE TABLE food_item(
    item_id INT(8) NOT NULL AUTO_INCREMENT,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT,
    name VARCHAR(50) NOT NULL,
    establishment_id INT(8),
    PRIMARY KEY(item_id),
    CONSTRAINT food_item_establishment_id_fk FOREIGN KEY(establishment_id) REFERENCES food_establishment(establishment_id)
);

CREATE TABLE food_review(
    review_id INT(8) NOT NULL AUTO_INCREMENT,
    review_text TEXT,
    rating INT(1) NOT NULL,
    `datetime` DATETIME DEFAULT NOW(),
    account_id INT(8) NOT NULL,
    establishment_id INT(8),
    item_id INT(8),
    PRIMARY KEY(review_id),
    CONSTRAINT food_review_account_id_fk FOREIGN KEY(account_id) REFERENCES customer(account_id),
    CONSTRAINT food_review_establishment_id_fk FOREIGN KEY(establishment_id) REFERENCES food_establishment(establishment_id),
    CONSTRAINT food_review_item_id_fk FOREIGN KEY(item_id) REFERENCES food_item(item_id),
    CONSTRAINT rating_range_check CHECK(
        rating >= 1
        AND rating <= 5
    )
);

CREATE TABLE food_item_food_type(
    item_id INT(8) NOT NULL,
    food_type VARCHAR(50) NOT NULL,
    PRIMARY KEY(item_id, food_type),
    CONSTRAINT food_item_food_type_item_id_fk FOREIGN KEY(item_id) REFERENCES food_item(item_id)
);

-- TEST DATA --
-- Customer insertion
-- bad email format
INSERT INTO
    customer
VALUES
    (1, "customer", "password", "customer@gugol.kom");

-- bad password format
INSERT INTO
    customer
VALUES
    (1, "customer", "password1", "customer");

-- valid
INSERT INTO
    customer
VALUES
    (1, "customer", "password1", "customer@gugol.kom");

-- Owner insertion
-- bad password format
-- INSERT INTO owner VALUES(1, "owner", "password", "customer@gugol.kom");
-- bad email format
-- INSERT INTO owner VALUES(1, "owner", "password1", "customer");
-- valid
INSERT INTO
    owner
VALUES
    (1, "owner", "password1", "customer@gugol.kom");

-- Food establishment insertion
-- account id does not exist
-- INSERT INTO food_establishment VALUES(1, "location", "description", 5, "name", 2);
-- valid
INSERT INTO
    food_establishment
VALUES
    (1, "location", "description", 5, "name", 1);

INSERT INTO
    food_establishment(
        location,
        description,
        average_rating,
        name,
        account_id
    )
VALUES
    ("location", "description", 5, "name", 1);

-- Food item insertion
-- establishment_id does not exist
-- INSERT INTO food_item VALUES(1, 100, "description", "name", 3);
-- valid
INSERT INTO
    food_item
VALUES
    (1, 100, "description", "name", 1, 1);