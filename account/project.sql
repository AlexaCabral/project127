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
    average_rating INT(2),
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
INSERT INTO customer (name, password, email) VALUES ("customer", "password", "customer@gugol.kom");

-- bad password format
INSERT INTO customer (name, password, email) VALUES ("customer", "password1", "customer");

-- valid
INSERT INTO customer (name, password, email) VALUES ("customer", "password1", "customer@gugol.kom");

-- Owner insertion
-- bad password format
-- INSERT INTO owner VALUES(1, "owner", "password", "customer@gugol.kom");
-- bad email format
-- INSERT INTO owner VALUES(1, "owner", "password1", "customer");
-- valid
INSERT INTO owner (name, password, email) VALUES ("owner", "password1", "customer@gugol.kom");

-- Food establishment insertion
-- account id does not exist
-- INSERT INTO food_establishment VALUES(1, "location", "description", 5, "name", 2);
-- valid

INSERT INTO food_establishment (location, description, average_rating, name, account_id)
VALUES 
    ("Manila", "The world's second-largest restaurant chain", 4, "KFC", 1),
    ("Los Baños", "The largest fast food chain branch in the Philippines", 5, "Jollibee", 1),
    ("Makati", "An American multinational fast food chain", 3, "McDonald's", 1),
    ("Los Baños", "Home of the mouth-watering crunch and juicy fried chicken bursting with Louisiana flavor", 3, "Popeyes", 1),
    ("Batangas", "A multinational coffee houses and roastering based in Washington", 5, "Starbucks", 1),
    ("BGC", "A Cajun-inspired restaurant which specializes on exquisitely - flavored seafood", 2, "Orange Bucket", 1),
    ("Baguio", "A restaurant coined from the rhythmic cooking sound of okonomiyaki", 3, "Botejyu", 1),
    ("BGC", "Known for its twists on classic Filipino dishes", 4, "Manam", 1),
    ("Batangas", "Known for more than just their fluffy pancakes and delicious comfort food.", 4, "Pancake House", 1),
    ("Manila", "A Japanese fast-casual restaurant chain specializing in udon", 2, "Marugame Udon", 1)
    
;
-- Food item insertion
-- establishment_id does not exist
-- INSERT INTO food_item VALUES(1, 100, "description", "name", 3);
-- valid

-- KFC FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES 
    (70, "A fresh mix of vegetables with signature tangy dressing.", "Coleslaw Salad", 1),
    (130, "Crunchy Hot Shots matched with crispy fries and a drink.", "Shot Combo", 1),
    (180, "Drizzled with chicken sisig sauce, fried chicken skin, topped with mayo and egg with steamed rice and drink.", "Sisig Rice Bowl Meal", 1),
    (354, "Chizza with 1 pc chicken with rice, gravy and drink.", "KFC Chizza Fully Loaded Meal", 1),
    (120, "A twister with chicken shots wrapped in tortilla with mango bits.", "California Maki Twister", 1),
    (60, "Creamy mashed potato topped with gravy.", "Mashed Potato", 1),
    (155, "A big spicy sandwich made with zinger chicken fillet.", "Zinger", 1)
;
-- JOLLIBEE FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES 
    (165, "Tender beef tapa served with garlic rice and fried egg", "Beef Tapa", 2),
    (82, "2 pieces of moist pancakes served with butter and maple syrup.", "Pancakes", 2),
    (80, "Iced coffee, freshly brewed made from 100% Arabica beans, mixed with creamy chocolate", "Iced Mocha Float", 2),
    (63, "Creamy vanilla soft serve topped with chewy buko pandan jelly, buko strips, and pandan syrup.", "Buko pandan sundae", 2),
    (449, "A bucket of your favorite crispylicious, juicylicious Chickenjoy!", "6 - pc. Chickenjoy Solo", 2),
    (164, "Meatiest, cheesiest, and sweet-sarap Jolly Spaghetti good for sharing", "Jolly Spaghetti Family Pan", 2),
    (61, "Soda Float", "Coke float", 2)
;

-- MCDONALDS FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES 
    (95, "Classic cheese burger", "Cheeseburger Deluxe", 3),
    (37, "Classic burger with beefier patty.", "Burger McDo", 3),
    (178, "6 chicken nuggets with bbq sauce and crunchy fries", "Chicken McNuggets with Fries", 3),
    (57, "Crunchy chocolate double oreo, creamy delight", "McFlurry", 3),
    (110, "Sizzling sausage, fresh grade a egg and american cheese on english muffin", "Sausage McMuffin with Egg", 3),
    (164, "Fries for sharing", "BFF Fries", 3),
    (61, "A premium roast coffee", "McCafe Premium Roast Coffee", 3)
;
    
-- POPEYES FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES 
    (53, "Light, hearty, and flaky buttermilk biscuits with rich honey drizzle", "Honey Biscuit", 4),
    (167, "Delicious breaded shrimp patty wt a tangy mayo sauce", "Shrimp Burger", 4),
    (84, "5 pcs of mac n cheese with jalapeño bits, balled up and deep-fried to perfection", "Regular Mac N Cheese Hot Pops", 4),
    (180, "Four types of cocoa beverages blended with steamed milk and topped with a sprinkle of chocolate powder.", "Signature Chocolate", 4),
    (89, "A fluffy pancake", "Fluffy Pancake", 4),
    (393, "10 pcs chicken tenders, marinated in Louisiana seasonings", "10-pcs Tenders", 4),
    (236, "Chicken french quarter burger served with regular crispy Cajun fries and iced tea", "Chicken French Quarte Regular Meal", 4)
;

-- STARBUCKS'S FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES 
    (195, "A blend of steamed milk infused with vanilla syrup is paired with a shot of espresso and finished with a delightful caramel drizzle on top.", "Caramel Macchiato", 5),
    (180, "Iced coffee made in small batches, steeped slowly for 20 hours.", "Cold Brew", 5),
    (160, "Espresso shots blended with steaming hot water.", "Caffe Americano", 5),
    (180, "Four types of cocoa beverages blended with steamed milk and topped with a sprinkle of chocolate powder.", "Signature Chocolate", 5),
    (284, "The timeless lasagna crafted with a robust plant-based ground patty", "Plant-based Classic Lasagna", 5),
    (120, "A fusion of bold espresso, decadent mocha sauce, and velvety steamed milk.", "Caffe Mocha", 5),
    (284, "Custom blended cold brew, meticulously slow-steeped, crowned with our signature house-made vanilla sweet cream.", "Vanilla Sweet Cream Cold Brew", 5)
;

-- ORANGE BUCKET FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES
    (1999, "Bucket with 500g crab, 400g shrimp, 400g mussels, 400g scallops, 200g potato and 3pcs corn", "The Big Bang Seafood Bucket Classic", 6),
    (2299, "Bucket with 500g lobster, 400g shrimp, 400g mussels, 400g scallops, 200g potato and 3pcs corn", "The Big Bang Seafood Bucket Premium", 6),
    (1599, "Bucket with 500g crab, 400g shrimp, 400g mussels, 300g scallops, 200g potato and 2pcs corn", "Signature Seafood Bucket", 6),
    (379, "Shrimp soup with mushrooms and cilantro, topped with coconut milk", "Tom Yang Goong Soup", 6),
    (1299, "Orange crustacean sheeted in a delicate layer of salted egg sauce", "Salted Egg Crab", 6),
    (475, "12 pcs Fried chicken wings tossed in buffalo sauce", "Tob Buffalo Wings", 6),
    (355, "A salad specially prepared by our Chef", "Chef's Salad", 6)
;

-- BOTEJYU FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES
   (675, "Rice topped with sliced beef garlic steak", "Diced Beef Garlic Steak Rice Bowl", 7),
   (330, "Rice topped with chicken sauteed in butter and umami sauce", "Chicken Butter Rice Bowl", 7),
   (575, "Beef cooked in special umami sukiyaki sauce with soft boiled egg rice set", "Sukiyaki Beef Teishoku", 7),
   (430, "Salmon", "Pressed Salmon Sushi", 7),
   (400, "Eel, Avocado, Lettuce", "Unagi & Avocado Roll", 7),
   (4995, "Premium Japanese Wagyu Steak in Osaka style", "Japanese Wagyu Steak Osaka Style", 7),
   (5995, "Grilled Beef and Pork Steak Platter", "Grilled Mixed Yakiniku Steak Platter", 7)
;


-- MANAM FOOD ITEMS

INSERT INTO food_item (price, description, name, establishment_id)
VALUES
   (125, "Tinapa flakes, mangga't bagoong, pomelo, native tomatoes, red onions, peanuts,tossed.", "Enseladang Namnam", 8),
   (200, "Eggplant, tomato, longganisa, omelette, fried", "Tortang Talong with Longganisa", 8),
   (375, "Crab, prawns, tanigue, squid, mussels, in a peanut stew with house-made vegetables ukoy fritters", "Seafood Bounty Kare-Kare", 8),
   (335, "Deep-fried pork knuckles in a sweet soy glaze", "Crispy Pata Tim", 8),
   (245, "A namnam favorite and an original family recipe", "Sinigang na Beef Short Rib & Watermelon", 8),
   (180, "Squid ink and crunchy garlic bits mixed with bihon noodles cooked in shrimp broth", "Pancit Negra", 8),
   (185, "All-day breakfast for champion", "Corned Beef Sisig", 8)
;

-- PANCAKE HOUSE FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES
   (199, "Chocolate syrup-swirled pancakes for just the right touch of sweetness", "Chocolate Marble Pancakes", 9),
    (189, "Classic and crispy delicious golden brown waffle", "Golden Brown Waffle", 9),
    (265, "Flavorful brown rice pilaf paired with tender chicken paillard and garnished with garlic cream mayo, chopped parsley, and lemon wedge", "Spicy Chicken Fillet With Brown Rice", 9),
    (325, "Milkfish smoked to golden perfection and served with steamed rice and mango salsa", "Smoked Golden Tinapa", 9),
    (284, "Premium 1/3 lb salisbury steak topped with creamy mushroom gravy and bacon bits", "Special Salisbury Steak", 9),
    (120, "Colorful South of the Border Mexican treat! Ground beef, lettuce, tomato, onion and cheese in crispy taco shell", "Best Taco in Town", 9),
    (284, "Breaded lean pork, finely sliced and served with rice and coleslaw", "Pork Vienna", 9)
;

-- MARUGAME UDON FOOD ITEMS
INSERT INTO food_item (price, description, name, establishment_id)
VALUES
  (235, "Cooked Japanese Rice topped with sliced beef and pickled ginger.", "Gyudon Rice Bowl", 10),
  (75, "Japanese rice wrapped with nori sheet and spam", "Spam Omusubi", 10),
  (250, "Drizzled with chicken sisig sauce, fried chicken skin, topped with mayo and egg with steamed rice and drink", "Beef Ontama Bukkake Udon", 10),
  (250, "Japanese summer dish consisting of udon noodles", "Zaru Udon", 10),
  (215, "Freshly made udon, topped with curry beef.", "Curry Udon", 10),
  (75, "Fried Marinated Chicken", "Chicken Karaage", 10),
  (80, "Fried Shrimp in Tempura Butter", "Ebi Ten", 10)
;