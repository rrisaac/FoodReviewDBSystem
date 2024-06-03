DROP DATABASE IF EXISTS food;

CREATE DATABASE food;

USE food;

CREATE TABLE user(
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    user_username VARCHAR(30) NOT NULL,
    user_password VARCHAR(30) NOT NULL,

    CONSTRAINT user_username_uk UNIQUE KEY(user_username)  
);


CREATE TABLE foodEstablishment(
    establishment_id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_name VARCHAR(30) NOT NULL,
    establishment_averagerating DECIMAL(3,2) DEFAULT 0,

    CONSTRAINT foodEstablishment_establishment_name_uk UNIQUE KEY(establishment_name)
);

CREATE TABLE foodItem(
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(30) NOT NULL,
    food_type VARCHAR(255) NOT NULL,
    food_price DECIMAL(6,2) DEFAULT 0,
    food_averagerating DECIMAL(3,2) DEFAULT 0,
    food_foodestablishmentid INT NOT NULL,

    -- when an establishment gets deleted, the food that the food establishment has is deleted
    CONSTRAINT food_foodestablishmentid_fk FOREIGN KEY(food_foodestablishmentid) REFERENCES foodEstablishment(establishment_id) ON DELETE CASCADE,

    CONSTRAINT food_name_uk UNIQUE KEY(food_name)
);

CREATE TABLE foodReview(
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    review_type DECIMAL(1) NOT NULL,  -- (0) establishment, (1) item
    review_message VARCHAR(255) NOT NULL, 
    review_date DATE NOT NULL,
    review_rating DECIMAL(3,2) DEFAULT 0,
    review_fooditemid INT, 
    review_foodestablishmentid INT, 
    review_userid INT NOT NULL, 

    -- when a food item gets deleted, the food review of the user pertaining to that food item is also deleted
    CONSTRAINT review_fooditemid_fk FOREIGN KEY(review_fooditemid) REFERENCES foodItem(food_id) ON DELETE CASCADE,

    -- when a food establishment is deleted, the food review of the user pertaining to that food establishment is also deleted
    CONSTRAINT review_foodestablishmentid_fk FOREIGN KEY(review_foodestablishmentid) REFERENCES foodEstablishment(establishment_id) ON DELETE CASCADE,

    -- when a user is deleted, all the food review of that user are also deleted
    CONSTRAINT review_userid_fk FOREIGN KEY(review_userid) REFERENCES user(user_id) ON DELETE CASCADE  
);

-- DESC user;

-- DESC foodEstablishment;

-- DESC foodItem;

-- DESC foodReview;

-- Dummy values:

INSERT INTO foodEstablishment (establishment_name)
VALUES
    ('Jollibee Calamba'),
    ('Panda Express'),
    ('Dairy Queen'),
    ('Jollibee Los Banos'),
    ('McDonald''s'),    
    ('Burger King'),
    ('KFC'),
    ('Goldilocks'),
    ('Wendy''s'),
    ('Max''s Restaurant'),
    ('Pizza Hut'),
    ('Domino''s Pizza'),
    ('Dunkin'' Donuts'),
    ('Starbucks'),
    ('Mang Inasal'),
    ('Chowking'),
    ('Barrio Fiesta'),
    ('Gerry''s Grill'),
    ('Red Ribbon'),
    ('Kuya J');


INSERT INTO user (user_username, user_password)
VALUES
    ('Maria_DelRosario', '123456'),
    ('JuanitoMagsaysay', 'admin'),
    ('CarlaPanganiban', '12345678'),
    ('MiguelitoDelaCruz', '123456789'),
    ('AnnaKapunanPH', '1234'),
    ('JoseRizalFanatic', '12345'),
    ('IsabelaSantos123', 'password'),
    ('RonaldoDiazPinoy', '123'),
    ('SofiaLopezCordova', 'Aa123456'),
    ('MateoMagnoPH', '1234567890'),
    ('TeresaGonzales', 'UNKNOWN'),
    ('EduardoDeLeon_', '1234567'),
    ('KatrinaVelasquez', '123123'),
    ('AndresBonifacio_', '111111'),
    ('LorraineSantiagoPH', 'Password'),
    ('AngeloGarciaPinoy', '12345678910'),
    ('AndreaAlcantara_', '0'),
    ('GabrielTorresPH', 'Admin123'),
    ('MaricarLuna', '********'),
    ('PaoloSantosOnline', 'user');

INSERT INTO foodItem (food_name, food_type, food_price, food_foodestablishmentid)
VALUES
    ('Cheeseburger', 'Meat,Dairy,Bread', 66.00, 5),
    ('Jolly Spaghetti', 'Meat,Pasta', 60.25, 1),
    ('Pizza', 'Dairy,Bread,Meat,Veg', 472.50, 11),
    ('Halo-Halo', 'Dairy,Fruit,Ice', 82.75, 10),
    ('Blizzard', 'Dairy,Ice', 150.80, 3),
    ('Fried Chicken', 'Meat', 231.55, 7),
    ('Sinigang', 'Meat,Veg', 265.30, 10),
    ('Hamburger', 'Meat,Bread', 146.90, 6),
    ('Palabok', 'Meat,Seafood,Noodles', 72.45, 4),
    ('Chickenjoy', 'Meat', 99.70, 4),
    ('Siopao', 'Meat,Bread', 45.35, 16),
    ('French Fries', 'Veg', 65.55, 5),
    ('Bicol Express', 'Meat,Veg', 294.20, 17),
    ('Lumpiang Shanghai', 'Meat,Veg', 243.85, 1),
    ('Sisig', 'Meat', 152.40, 20),
    ('Pork BBQ', 'Meat', 308.65, 15),
    ('Whopper', 'Meat,Bread,Veg', 200.50, 6),
    ('Dinuguan', 'Meat', 300.75, 20),
    ('Crispy Pata', 'Meat', 655.90, 18),
    ('Cake', 'Dairy,Bread', 785.25, 8);

INSERT INTO foodReview (review_type, review_message, review_date, review_rating, review_fooditemid, review_foodestablishmentid, review_userid)
VALUES
    (0, 'The establishment provided excellent service, very satisfied!', '2024-05-01', 3.76, NULL, 1, 5),
    (1, 'Taste good bread, satisfied!', '2024-02-15', 0.54, 8, NULL, 12),
    (1, 'Satisfactory item quality, will visit again.', '2024-09-23', 2.10, 20, NULL, 3),
    (0, 'Poor service experience, needs improvement.', '2024-07-10', 1.32, NULL, 20, 17),
    (0, 'Delicious food, highly recommended!', '2024-03-08', 4.65, NULL, 10, 9),
    (1, 'Disappointed with the item, not up to expectations.', '2024-11-30', 1.98, 7, NULL, 5),
    (0, 'Great ambiance, but service was lacking.', '2024-06-19', 0.87, NULL, 14, 14),
    (1, 'Fantastic taste, worth every penny!', '2024-04-05', 4.09, 19, NULL, 8),
    (1, 'Item received was fresh and tasty, satisfied!', '2024-10-12', 2.43, 4, NULL, 1),
    (0, 'Service was slow, but the food was good.', '2024-08-25', 3.54, NULL, 9, 11),
    (0, 'Unsatisfactory experience overall, needs improvement.', '2024-01-17', 0.21, NULL, 12, 5),
    (1, 'The item was not as described, disappointed.', '2024-12-04', 4.32, 19, NULL, 20),
    (1, 'Friendly staff, satisfied with the service.', '2024-07-28', 2.87, 2, NULL, 16),
    (0, 'Excellent food quality, will definitely return.', '2024-05-11', 1.76, NULL, 5, 7),
    (1, 'Item was delivered promptly, satisfied with the service.', '2024-03-29', 3.00, 10, NULL, 5),
    (0, 'Poor hygiene standards observed, not satisfied.', '2024-09-02', 0.34, NULL, 13, 18),
    (1, 'Tasty dishes, satisfied with the experience.', '2024-06-14', 4.21, 18, NULL, 13),
    (0, 'Disappointed with the food, didn''t meet expectations.', '2024-04-27', 2.65, NULL, 11, 10),
    (0, 'Good customer service, but the food was mediocre.', '2024-11-08', 1.45, NULL, 4, 2),
    (1, 'Highly satisfied with the quality of the item received.', '2024-08-01', 5.00, 2, NULL, 6);

