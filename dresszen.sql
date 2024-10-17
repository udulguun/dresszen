CREATE DATABASE dresszenfinder5;
USE dresszenfinder5;
-- Create Users table
CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    size VARCHAR(30) NOT NULL,
    email VARCHAR(50) NOT NULL,
    gender ENUM('Male', 'Female'),
    age INT,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);
-- Create Outfit table
CREATE TABLE Outfit (
    outfit_id INT NOT NULL AUTO_INCREMENT,
    Occasion ENUM('Casual', 'Formal', 'Sport', 'Business', 'Party') NOT NULL,
    PRIMARY KEY (outfit_id)
);
-- Create User_Comments table
CREATE TABLE User_Comments (
    comment_id INT NOT NULL AUTO_INCREMENT,
    user_id INT,
    outfit_id INT,
    content TEXT NOT NULL,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (outfit_id) REFERENCES Outfit(outfit_id) ON DELETE CASCADE
);
-- Create Interested_In table
CREATE TABLE Interested_In (
    user_id INT,
    outfit_id INT,
    PRIMARY KEY (user_id, outfit_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (outfit_id) REFERENCES Outfit(outfit_id) ON DELETE CASCADE
);
-- Create Clothing_Item table
CREATE TABLE Clothing_Item (
    cloth_id INT PRIMARY KEY AUTO_INCREMENT,
    size VARCHAR(20),
    color VARCHAR(255),
    cloth_description TEXT,
    brand_id INT,
    type ENUM('Top', 'Bottom', 'Accessory', 'Shoe')
);
-- Create Wardrobe table
CREATE TABLE Wardrobe (
    user_id INT,
    cloth_id INT,
    PRIMARY KEY (user_id, cloth_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (cloth_id) REFERENCES Clothing_Item(cloth_id) ON DELETE CASCADE
);
-- Create brands table
CREATE TABLE brands (
    brand_id INT NOT NULL AUTO_INCREMENT,
    brand_name VARCHAR(50),
    brand_website TEXT,
    type ENUM('Luxury', 'Sportswear', 'Fast Fashion') NOT NULL,
    PRIMARY KEY (brand_id)
);
-- Create User_Rating table
CREATE TABLE User_Rating (
    user_id INT,
    cloth_id INT,
    rating TINYINT CHECK (
        rating >= 1
        AND rating <= 5
    ),
    PRIMARY KEY (user_id, cloth_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (cloth_id) REFERENCES Clothing_Item(cloth_id) ON DELETE CASCADE
);
-- Create Outfit_Clothing_Item table
CREATE TABLE Outfit_Clothing_Item (
    outfit_id INT,
    cloth_id INT,
    PRIMARY KEY (outfit_id, cloth_id),
    FOREIGN KEY (outfit_id) REFERENCES Outfit(outfit_id) ON DELETE CASCADE,
    FOREIGN KEY (cloth_id) REFERENCES Clothing_Item(cloth_id) ON DELETE CASCADE
);
-- Create belongs_to table
CREATE TABLE belongs_to (
    cloth_id INT,
    brand_id INT,
    PRIMARY KEY (cloth_id, brand_id),
    FOREIGN KEY (cloth_id) REFERENCES Clothing_Item(cloth_id) ON DELETE CASCADE,
    FOREIGN KEY (brand_id) REFERENCES brands(brand_id) ON DELETE CASCADE
);
ALTER TABLE users
MODIFY username VARCHAR(50) NULL,
    MODIFY size VARCHAR(30) NULL,
    MODIFY email VARCHAR(50) NULL,
    MODIFY gender ENUM('Male', 'Female') NULL,
    MODIFY age INT NULL,
    MODIFY password VARCHAR(255) NULL;
USE dresszenfinder5;
SELECT *
FROM users;
drop DATABASE dresszenfinder5;